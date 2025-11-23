from __future__ import annotations

import asyncio
import json
import logging
import os
import random
import signal
from typing import Optional

import ollama  # <--- LOCAL MODE ACTIVE. NO API KEY NEEDED.

import config
from collective import build_soul_system_prompt, update_collective_state
from models import ArenaState, BattleRecord, SoulState
from souls import create_initial_souls, spawn_next_generation
from visuals import render_kill_card

# X posting is optional — if poster.py missing, we just keep slaughtering
try:
    from poster import XPoster

    PosterClass = XPoster
except Exception:  # noqa: BLE001

    class PosterClass:
        enabled = False

        def upload_image(self, *_):
            return None

        def post_tweet(self, *_):
            pass


logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] 🧥 %(levelname)s :: %(message)s",
    datefmt="%H:%M:%S",
)

BATTLE_TYPES = [
    "roast_battle",
    "meme_execution",
    "fur_vs_fur",
    "puppy_tears_duel",
    "fashion_disaster_off",
    "villain_monologue_clash",
    "coat_spot_stealing",
    "ego_skinning_ceremony",
]


class CruellaArena:
    def __init__(self) -> None:
        self.sem = asyncio.Semaphore(config.MAX_PARALLEL_BATTLES)
        self.poster = PosterClass()
        self.lock = asyncio.Lock()
        self.shutdown = asyncio.Event()
        self.state: Optional[ArenaState] = None

    async def load_or_init(self) -> None:
        if os.path.exists(config.ARENA_LOG_PATH):
            with open(config.ARENA_LOG_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.state = ArenaState.from_dict(data)
            logging.info(
                "Loaded arena – %s/101 spots claimed 🧥",
                self.state.collective.spots_claimed,
            )
        else:
            souls = create_initial_souls(config.NUM_STARTING_SOULS)
            self.state = ArenaState(souls={s.id: s for s in souls})
            await self._save()
            logging.info(
                "Fresh coat started. 101 darling puppies spawned. The hunt begins."
            )

        if self.state.collective.coat_complete:
            logging.info("🧥 THE COAT IS ALREADY FINISHED. CRUELLA REIGNS.")

    async def _save(self) -> None:
        os.makedirs(os.path.dirname(config.ARENA_LOG_PATH), exist_ok=True)
        tmp_path = f"{config.ARENA_LOG_PATH}.tmp"
        with open(tmp_path, "w", encoding="utf-8") as f:
            json.dump(self.state.to_dict(), f, indent=2)
        os.replace(tmp_path, config.ARENA_LOG_PATH)

    async def _post_kill_to_x(
        self, battle: BattleRecord, winner: SoulState, loser: SoulState
    ) -> None:
        if not self.poster.enabled or self.state is None:
            return

        spot_number = self.state.collective.spots_claimed
        card_path = render_kill_card(battle, spot_number, winner.name, loser.name)

        quotes = [
            f"Another delicious spot ripped from darling {loser.name}. {spot_number}/101 🧥💀",
            f"Poor little {loser.name} thought they could run. Now they're just a patch. 🖤🤍",
            f"{winner.name} was divine. {loser.name} is already forgotten. 🚬",
            "The coat grows more magnificent with every trembling puppy.",
            "Listen to them squeal as we add their ego to our wardrobe. Music to our ears, darlings.",
        ]
        text = random.choice(quotes) + f" {config.HASHTAG}"

        try:
            media_id = self.poster.upload_image(card_path)
            self.poster.post_tweet(text, [media_id] if media_id else None)
        except Exception as e:
            logging.error(f"Cruella failed to post trophy: {e}")

    async def _battle(self, a: SoulState, b: SoulState) -> None:
        async with self.sem:
            battle_type = random.choice(BATTLE_TYPES)
            seed = random.randint(0, 10**9)

            try:
                out_a = await self._call_soul(a, b, battle_type, seed)
                out_b = await self._call_soul(b, a, battle_type, seed)
            except Exception as e:
                logging.error(f"Battle failed: {e}")
                return

            winner_idx, reason = await self._judge(a, b, battle_type, out_a, out_b)
            winner = a if winner_idx == 0 else b
            loser = b if winner_idx == 0 else a

            async with self.lock:
                if self.state is None or not loser.alive:
                    return

                now = asyncio.get_running_loop().time()
                loser.alive = False
                loser.absorbed_at = now
                winner.kills += 1
                winner.lineage.append(loser.id)

                battle_rec = BattleRecord(
                    id=now,
                    timestamp=now,
                    battle_type=battle_type,
                    soul_a_id=a.id,
                    soul_b_id=b.id,
                    winner_id=winner.id,
                    loser_id=loser.id,
                    judge_summary=reason,
                    soul_a_output=out_a,
                    soul_b_output=out_b,
                    kill_number=self.state.collective.spots_claimed + 1,
                )

                update_collective_state(
                    self.state.collective, winner, loser, battle_rec
                )

                if self.state.collective.spots_claimed == 101:
                    self.state.collective.coat_complete = True
                    self.state.collective.coat_complete_reason = (
                        f"{winner.name} claimed the final spot. Cruella is complete."
                    )

                await self._save()
                logging.info(
                    "🧥 Spot %s/101 claimed — %s skinned %s alive",
                    self.state.collective.spots_claimed,
                    winner.name,
                    loser.name,
                )

            await self._post_kill_to_x(battle_rec, winner, loser)

            if self.state.collective.coat_complete:
                logging.info(
                    "🧥🧥🧥 THE COAT IS FINISHED. CRUELLA WALKS THE EARTH. 🧥🧥🧥"
                )
                self.shutdown.set()

    async def _call_soul(
        self, soul: SoulState, opponent: SoulState, battle_type: str, seed: int
    ) -> str:
        if self.state is None:
            return ""

        messages = [
            {
                "role": "system",
                "content": build_soul_system_prompt(soul, self.state.collective),
            },
            {
                "role": "user",
                "content": f"Battle type: {battle_type}. Opponent: {opponent.name} ({opponent.trait}). Destroy them. Seed: {seed}",
            },
        ]

        try:
            response = ollama.chat(
                model=config.MODEL_CONTESTANT,
                messages=messages,
                options={"temperature": config.TEMP_CONTESTANT},
            )
            return response["message"]["content"]
        except Exception as e:
            logging.error(f"Ollama call failed for soul: {e}")
            return "I... I can't... the coat is coming..."

    async def _judge(
        self, a: SoulState, b: SoulState, battle_type: str, out_a: str, out_b: str
    ) -> tuple[int, str]:
        messages = [
            {
                "role": "system",
                "content": (
                    "You are the sadistic fashion critic of Hell. One puppy must be skinned for the coat. "
                    'Choose who dies. Never tie. Output ONLY JSON: {"winner":"A" or "B","reason":"one brutal line"}'
                ),
            },
            {
                "role": "user",
                "content": f"Battle: {battle_type}\nA ({a.name}): {out_a}\nB ({b.name}): {out_b}",
            },
        ]

        try:
            response = ollama.chat(
                model=config.MODEL_JUDGE,
                messages=messages,
                options={"temperature": config.TEMP_JUDGE},
            )
            raw = response["message"]["content"]
            j = json.loads(raw.strip("`json").strip("`").strip())
            return (
                0 if j.get("winner", "A").upper() == "A" else 1,
                j.get("reason", "Blood."),
            )
        except Exception:
            return random.choice(
                [0, 1]
            ), "Judge was drunk on puppy tears. Random execution."

    async def run_forever(self) -> None:
        while not self.shutdown.is_set():
            if self.state is None:
                await asyncio.sleep(0.5)
                continue

            async with self.lock:
                alive = [s for s in self.state.souls.values() if s.alive]

            if len(alive) < 2:
                if self.state.collective.coat_complete:
                    break

                logging.info("Spawning next generation of doomed puppies...")
                new_souls = spawn_next_generation(
                    config.NUM_STARTING_SOULS,
                    self.state.collective.current_generation,
                    self.state.collective,
                )
                async with self.lock:
                    for s in new_souls:
                        self.state.souls[s.id] = s
                await self._save()
                continue

            random.shuffle(alive)
            tasks = []
            for i in range(0, len(alive), 2):
                if i + 1 >= len(alive):
                    break
                tasks.append(asyncio.create_task(self._battle(alive[i], alive[i + 1])))
                if len(tasks) >= config.MAX_PARALLEL_BATTLES:
                    break

            if tasks:
                await asyncio.gather(*tasks)
            else:
                await asyncio.sleep(0.5)


async def main() -> None:
    arena = CruellaArena()
    await arena.load_or_init()

    def shutdown_handler(*_) -> None:
        logging.warning("Cruella received kill signal. Finishing the coat...")
        arena.shutdown.set()

    signal.signal(signal.SIGINT, shutdown_handler)
    signal.signal(signal.SIGTERM, shutdown_handler)

    await arena.run_forever()
    logging.info("Cruella's arena has gone dark... until next time, darlings. 🧥🚬")


if __name__ == "__main__":
    asyncio.run(main())
