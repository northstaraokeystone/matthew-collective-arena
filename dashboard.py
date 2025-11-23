# ruff: noqa: E501
from __future__ import annotations

import json
import logging
import re
import time
from typing import TYPE_CHECKING

import ollama
import streamlit as st

import config
from collective import build_coat_complete_prompt
from models import ArenaState

if TYPE_CHECKING:
    from models import CollectiveState

# Cruella demands this be the very first Streamlit command.
st.set_page_config(
    page_title="101 Matthews: Cruella's Ego Coat",
    page_icon="🧥",
    layout="wide",
)


def load_arena_state() -> ArenaState | None:
    """Peek into Cruella's mirrored arena log, darling."""
    try:
        with open(config.ARENA_LOG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return ArenaState.from_dict(data)
    except FileNotFoundError:
        return None
    except Exception as exc:  # noqa: BLE001
        logging.error("Cruella's mirror cracked: %s", exc)
        return None


def call_collective(system_prompt: str, user_prompt: str) -> str:
    """Whisper to the coat and force it to answer, darling."""
    messages: list[dict[str, str]] = [{"role": "system", "content": system_prompt}]
    user_clean = user_prompt.strip()
    if user_clean:
        messages.append({"role": "user", "content": user_clean})

    model_name = getattr(config, "MODEL_COLLECTIVE", "").strip()
    if not model_name:
        return (
            "The coat is unbound from any single model tonight, darling. "
            "Imagine the most vicious thing I could say and assume I said it."
        )

    try:
        response: dict[str, object] = ollama.chat(
            model=model_name,
            messages=messages,
            options={
                "temperature": config.TEMP_COLLECTIVE_ROAST,
                "num_predict": 320,
            },
        )
        content: str = ""

        message = response.get("message")
        if isinstance(message, dict):
            msg_content = message.get("content")
            if isinstance(msg_content, str):
                content = msg_content

        if not content:
            raw_response = response.get("response")
            if isinstance(raw_response, str):
                content = raw_response

        if not content:
            generic = response.get("content")
            if isinstance(generic, str):
                content = generic

        content = content.strip()
        if not content:
            return (
                "Cruella inhales, exhales, and decides you are beneath a full sentence, "
                "darling."
            )
        return content
    except Exception as exc:  # noqa: BLE001
        logging.error("Summoning Cruella failed: %s", exc)
        return (
            "Cruella is busy pinning a fresh spot to the coat. "
            "Try again in a moment, darling."
        )


def parse_kill_line(line: str) -> dict[str, str]:
    """Tear a kill snippet apart until it screams out names and spot numbers."""
    entry: dict[str, str] = {
        "raw": line,
        "spot": "???",
        "winner": "Cruella's Shadow",
        "loser": "a forgotten puppy",
        "verdict": "The coat simply took what it wanted.",
    }

    # Spot number — clean, no leading zeros
    spot_match = re.search(r"\[Spot\s+(\d+)", line)
    if spot_match:
        entry["spot"] = str(int(spot_match.group(1)))

    # Primary name extraction — Matthew names
    name_matches = re.findall(r"([A-Z][a-z]+ Matthew)", line)
    if len(name_matches) >= 2:
        entry["winner"] = name_matches[0].strip()
        entry["loser"] = name_matches[1].strip()

    # Fallback if winner missing
    if entry["winner"] == "Cruella's Shadow":
        for marker in (" flayed ", " reduced poor little ", " devoured ", " skinned "):
            if marker in line:
                left = line.split(marker, 1)[0]
                winner_raw = left.split("]", 1)[-1].strip()
                entry["winner"] = winner_raw.split("[", 1)[0].strip()
                break

    # Fallback if loser missing
    if entry["loser"] == "a forgotten puppy":
        if "'s ego" in line:
            loser_part = line.split("'s ego", 1)[0]
            entry["loser"] = loser_part.split(" ")[-1].strip().rstrip(".,")
        elif " to " in line:
            left, _ = line.split(" to ", 1)
            entry["loser"] = left.split(" ")[-1].strip().rstrip(".,")
        elif " over " in line:
            right = line.split(" over ", 1)[-1]
            entry["loser"] = right.split(" ")[0].strip().rstrip(".,:")

    # Verdict
    if "Verdict:" in line:
        entry["verdict"] = line.split("Verdict:", 1)[1].strip()
    else:
        dot_index = line.find(". ")
        if dot_index != -1:
            entry["verdict"] = line[dot_index + 2 :].strip()

    return entry


def build_kill_feed(collective: CollectiveState | None) -> list[dict[str, str]]:
    """Harvest the most recent fashion crimes from the coat's lining."""
    if not collective or not collective.essence:
        return []
    lines = [
        line.strip()
        for line in collective.essence.splitlines()
        if line.strip().startswith("[Spot")
    ]
    return [parse_kill_line(line) for line in lines[-50:][::-1]]


def inject_base_css(progress_pct: float, coat_complete: bool) -> None:
    """Drape the entire app in villain couture CSS, darling."""
    background_spots = (
        "radial-gradient(circle at 10% 20%, #ffffff20 0, #ffffff20 6px, transparent 7px), "
        "radial-gradient(circle at 80% 70%, #ffffff18 0, #ffffff18 7px, transparent 8px)"
    )
    fur_pattern = (
        "radial-gradient(circle at 15% 20%, #ffffff 0, #ffffff 9px, transparent 10px), "
        "radial-gradient(circle at 70% 60%, #ffffff 0, #ffffff 11px, transparent 12px), "
        "radial-gradient(circle at 40% 80%, #ffffff 0, #ffffff 10px, transparent 11px)"
    )

    coat_complete_css = ""
    if coat_complete:
        coat_complete_css = f"""
        [data-testid="stAppViewContainer"] {{
            background: #000000;
            background-image: {fur_pattern};
            background-size: 220px 220px;
            background-repeat: repeat;
        }}
        """

    st.markdown(
        f"""
        <style>
        html, body, [data-testid="stAppViewContainer"] {{
            background-color: #000000;
            color: #f5f5f5;
        }}
        [data-testid="stHeader"] {{
            background: transparent;
        }}
        .block-container {{
            padding-top: 1.5rem;
            padding-bottom: 1.5rem;
        }}

        .cruella-smoke-layer {{
            position: fixed;
            inset: 0;
            pointer-events: none;
            z-index: 9999;
            overflow: hidden;
        }}
        .cruella-smoke-dot {{
            position: absolute;
            width: 8px;
            height: 16px;
            border-radius: 50%;
            background: radial-gradient(circle at 30% 0%, #ffffff80 0, #ffffff20 30%, transparent 70%);
            opacity: 0.45;
            filter: blur(1px);
            animation: cruella-smoke-rise 18s linear infinite;
        }}
        .cruella-smoke-dot.s1 {{ left: 15%; animation-duration: 22s; }}
        .cruella-smoke-dot.s2 {{ left: 45%; animation-duration: 18s; }}
        .cruella-smoke-dot.s3 {{ left: 70%; animation-duration: 26s; }}
        .cruella-smoke-dot.s4 {{ left: 30%; animation-duration: 20s; }}
        .cruella-smoke-dot.s5 {{ left: 80%; animation-duration: 24s; }}
        @keyframes cruella-smoke-rise {{
            0% {{ transform: translateY(100vh); opacity: 0; }}
            20% {{ opacity: 0.5; }}
            80% {{ opacity: 0.4; }}
            100% {{ transform: translateY(-100vh); opacity: 0; }}
        }}

        .cruella-title {{
            font-family: "Cinzel", "Playfair Display", serif;
            font-size: 4.2rem;
            font-weight: 900;
            text-align: center;
            letter-spacing: 0.35em;
            text-transform: uppercase;
            margin: 1.5rem 0 0.5rem 0;
            background: linear-gradient(90deg, #8b0000, #ff1e1e, #8b0000);
            -webkit-background-clip: text;
            color: transparent;
            text-shadow: 0 0 25px #ff1e1e;
        }}
        .cruella-subtitle {{
            font-family: "Playfair Display", serif;
            text-align: center;
            font-size: 1.15rem;
            letter-spacing: 0.28em;
            color: #cccccc;
            margin-bottom: 2rem;
            font-style: italic;
        }}

        section[data-testid="stSidebar"] {{
            background: #050000;
            border-right: 1px solid #8b0000;
        }}

        .coat-progress-wrapper {{
            margin: 1rem 0 2.5rem 0;
            display: flex;
            align-items: flex-end;
            gap: 1.5rem;
        }}
        .coat-progress-bar {{
            position: relative;
            width: 60px;
            height: 260px;
            border-radius: 40px;
            border: 3px solid #ff1e1e;
            box-shadow: 0 0 35px rgba(255, 30, 30, 0.6);
            overflow: hidden;
            background:
                linear-gradient(to bottom, #1a0000 0%, #050000 40%, #000000 100%),
                {background_spots};
            background-size: 140px 140px, 220px 220px;
            background-position: center center;
        }}
        .coat-progress-fill {{
            position: absolute;
            left: 0;
            bottom: 0;
            width: 100%;
            height: {progress_pct:.2f}%;
            background:
                linear-gradient(180deg, #ff1e1e 0%, #8b0000 45%, #3b0000 100%);
            box-shadow: 0 0 30px rgba(255, 30, 30, 0.8);
            mix-blend-mode: screen;
        }}
        .coat-progress-text {{
            font-family: "Playfair Display", serif;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.18em;
            color: #f0f0f0;
        }}

        .kill-feed-title {{
            font-family: "Cinzel", serif;
            font-size: 1.7rem;
            text-align: center;
            letter-spacing: 0.22em;
            color: #ff1e1e;
            margin: 1.2rem 0 1.4rem 0;
            text-shadow: 0 0 18px #8b0000;
        }}
        .kill-card {{
            position: relative;
            margin: 0.9rem 0;
            padding: 1.2rem 1.6rem;
            border-radius: 18px;
            background:
                radial-gradient(circle at 10% 10%, #2a0000, #050000 60%),
                radial-gradient(circle at 90% 80%, #1c0000, #050000 70%);
            box-shadow:
                0 10px 32px rgba(0, 0, 0, 0.8),
                0 -4px 16px rgba(139, 0, 0, 0.6);
            border: 1px solid #3b0000;
            overflow: hidden;
            font-family: "Georgia", serif;
            color: #f2f2f2;
        }}
        .kill-card::before {{
            content: "";
            position: absolute;
            inset: 0;
            background-image:
                radial-gradient(circle at 15% 20%, #ffffff18 0, transparent 60%),
                radial-gradient(circle at 80% 60%, #ffffff10 0, transparent 50%);
            mix-blend-mode: screen;
            opacity: 0.8;
            pointer-events: none;
        }}
        .kill-card::after {{
            content: "";
            position: absolute;
            top: -18px;
            left: 0;
            right: 0;
            height: 34px;
            background:
                radial-gradient(circle at 10% 0, #ff1e1e80 0, transparent 55%),
                radial-gradient(circle at 40% 0, #ff1e1ea0 0, transparent 60%),
                radial-gradient(circle at 70% 0, #ff1e1e70 0, transparent 55%);
            opacity: 0;
            transition: opacity 0.5s ease-out;
            pointer-events: none;
        }}
        .kill-card-newest::after {{
            opacity: 1;
        }}

        .kill-card-burn-0 {{
            box-shadow: 0 10px 32px rgba(0, 0, 0, 0.9), 0 0 0 1px #2b0000;
        }}
        .kill-card-burn-0 .burn-spot-tl,
        .kill-card-burn-0 .burn-spot-br {{
            position: absolute;
            width: 22px;
            height: 22px;
            border-radius: 50%;
            background: radial-gradient(circle, #000000 0, #222222 35%, transparent 70%);
            box-shadow: 0 0 0 2px #440000, 0 0 16px rgba(255, 30, 30, 0.7);
        }}
        .kill-card-burn-0 .burn-spot-tl {{ top: -8px; left: 14px; }}
        .kill-card-burn-0 .burn-spot-br {{ bottom: -10px; right: 18px; }}

        .kill-card-burn-1 .burn-spot-tr,
        .kill-card-burn-1 .burn-spot-bl {{
            position: absolute;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: radial-gradient(circle, #000000 0, #1a1a1a 40%, transparent 70%);
            box-shadow: 0 0 0 2px #4b0000, 0 0 18px rgba(255, 30, 30, 0.6);
        }}
        .kill-card-burn-1 .burn-spot-tr {{ top: -10px; right: 22px; }}
        .kill-card-burn-1 .burn-spot-bl {{ bottom: -12px; left: 20px; }}

        .kill-card-burn-2 .burn-spot-center {{
            position: absolute;
            width: 26px;
            height: 26px;
            right: 40px;
            top: 12px;
            border-radius: 50%;
            background: radial-gradient(circle, #000000 0, #222222 40%, transparent 80%);
            box-shadow: 0 0 0 2px #550000, 0 0 16px rgba(255, 30, 30, 0.7);
        }}

        .kill-card-spot {{
            font-family: "Cinzel", serif;
            font-size: 0.95rem;
            letter-spacing: 0.28em;
            color: #ffb3b3;
            text-transform: uppercase;
            margin-bottom: 0.6rem;
        }}
        .kill-card-spot span {{
            padding: 0.15rem 0.75rem;
            border-radius: 999px;
            border: 1px solid #ff1e1e;
            text-shadow: 0 0 8px #ff1e1e;
        }}
        .kill-card-names {{
            font-size: 1.25rem;
            margin-bottom: 0.5rem;
        }}
        .gold-text {{
            color: #d4af37;
            text-shadow: 0 0 6px rgba(212, 175, 55, 0.9), 0 0 16px rgba(255,255,255,0.4);
        }}
        .silver-text {{
            color: #cccccc;
            text-shadow: 0 0 6px rgba(204, 204, 204, 0.9), 0 0 16px rgba(255,255,255,0.3);
        }}
        .kill-versus {{
            margin: 0 0.5rem;
            color: #ff1e1e;
        }}
        .kill-verdict {{
            font-family: "Playfair Display", serif;
            font-style: italic;
            font-size: 1rem;
            color: #f6f6f6;
            margin-top: 0.3rem;
        }}
        .kill-raw {{
            font-size: 0.8rem;
            color: #bbbbbb;
            opacity: 0.7;
            margin-top: 0.4rem;
        }}

        div[data-testid="stProgressBar"] {{
            visibility: hidden;
            height: 0;
            margin: 0;
        }}

        {coat_complete_css}
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="cruella-smoke-layer">
            <div class="cruella-smoke-dot s1"></div>
            <div class="cruella-smoke-dot s2"></div>
            <div class="cruella-smoke-dot s3"></div>
            <div class="cruella-smoke-dot s4"></div>
            <div class="cruella-smoke-dot s5"></div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def main() -> None:
    state = load_arena_state()
    collective: CollectiveState | None = state.collective if state else None
    spots_claimed = collective.spots_claimed if collective else 0
    total_spots = getattr(config, "NUM_STARTING_SOULS", 101) or 101
    coat_complete = bool(collective.coat_complete) if collective else False
    tagline = collective.tagline if collective else "The coat hungers."
    kill_count = collective.kill_count if collective else 0

    progress_pct = (
        min(max(spots_claimed / float(total_spots), 0.0), 1.0) * 100.0
        if total_spots > 0
        else 0.0
    )

    inject_base_css(progress_pct=progress_pct, coat_complete=coat_complete)

    # Sidebar
    with st.sidebar:
        st.markdown("### 🧥 Coat Status")
        st.markdown(f"**Spots Claimed**  \n`{spots_claimed}/{total_spots}`")
        st.markdown(f"**Total Kills**  \n`{kill_count}`")
        st.markdown("---")
        st.markdown("**Current Whisper**")
        st.markdown(f"_{tagline}_")

    # Header
    title_text = (
        "THE COAT IS FINISHED"
        if coat_complete
        else f"{spots_claimed}/{total_spots} SPOTS CLAIMED"
    )
    st.markdown(
        f'<div class="cruella-title">{title_text}</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        """
        <div class="cruella-subtitle">
            WATCH THE PUPPIES FALL, DARLING. THIS IS NOT A DASHBOARD. THIS IS A CRIME SCENE.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Progress
    st.markdown("#### Coat Completion")
    st.markdown(
        """
        <div class="coat-progress-wrapper">
            <div class="coat-progress-bar">
                <div class="coat-progress-fill"></div>
            </div>
            <div class="coat-progress-text">
                Each rise is another Matthew sewn screaming into the pattern.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.progress(spots_claimed / total_spots if total_spots else 0.0)

    col_left, col_right = st.columns([2, 1])

    # Kill feed
    with col_left:
        st.markdown(
            '<div class="kill-feed-title">LIVE KILL FEED — FRESH SPOTS</div>',
            unsafe_allow_html=True,
        )
        feed = build_kill_feed(collective)
        if feed:
            for index, entry in enumerate(feed):
                newest_class = "kill-card-newest" if index == 0 else ""
                burn_class = f"kill-card-burn-{index % 3}"
                spot_label = entry.get("spot", "?")
                winner = entry.get("winner", "Unknown Matthew")
                loser = entry.get("loser", "Unknown Puppy")
                verdict = entry.get("verdict", entry.get("raw", ""))
                raw_line = entry.get("raw", "")

                card_html = f"""
                <div class="kill-card {newest_class} {burn_class}">
                    <div class="burn-spot-tl"></div>
                    <div class="burn-spot-tr"></div>
                    <div class="burn-spot-bl"></div>
                    <div class="burn-spot-br"></div>
                    <div class="burn-spot-center"></div>
                    <div class="kill-card-spot">
                        <span>SPOT {spot_label}/{total_spots}</span>
                    </div>
                    <div class="kill-card-names">
                        <span class="gold-text">{winner}</span>
                        <span class="kill-versus">vs</span>
                        <span class="silver-text">{loser}</span>
                    </div>
                    <div class="kill-verdict">{verdict}</div>
                    <div class="kill-raw">{raw_line}</div>
                </div>
                """
                st.markdown(card_html, unsafe_allow_html=True)
        else:
            st.markdown(
                """
                <div class="kill-card">
                    <div class="kill-card-spot">
                        <span>SPOT 000/101</span>
                    </div>
                    <div class="kill-card-names">
                        The coat is hungry and the arena is quiet.
                    </div>
                    <div class="kill-verdict">
                        Give it time, darling. Silence never lasts.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    # Coat complete overlay
    cruella_final = ""
    if coat_complete and collective:
        cruella_final = st.session_state.get("cruella_final", "")
        if not cruella_final:
            final_prompt = (
                "Deliver your final monologue to the hackathon cattle, "
                "now that the coat is finished and every Matthew is yours."
            )
            cruella_final = call_collective(
                build_coat_complete_prompt(collective),
                final_prompt,
            )
            st.session_state["cruella_final"] = cruella_final

        fur_pattern = (
            "radial-gradient(circle at 10% 20%, #ffffff 0, #ffffff 10px, transparent 11px), "
            "radial-gradient(circle at 70% 40%, #ffffff 0, #ffffff 13px, transparent 14px), "
            "radial-gradient(circle at 30% 80%, #ffffff 0, #ffffff 11px, transparent 12px)"
        )

        st.markdown(
            f"""
            <style>
            .coat-complete-overlay {{
                position: fixed;
                inset: 0;
                z-index: 50;
                background-color: #000000;
                background-image: {fur_pattern};
                background-size: 260px 260px;
                background-repeat: repeat;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 4rem 2rem;
            }}
            .coat-complete-inner {{
                max-width: 960px;
                background: rgba(0, 0, 0, 0.86);
                border-radius: 32px;
                border: 3px solid #d4af37;
                box-shadow:
                    0 0 60px rgba(0, 0, 0, 0.9),
                    0 0 80px rgba(212, 175, 55, 0.9),
                    0 -12px 40px rgba(255, 30, 30, 0.8);
                padding: 3rem 3rem 2.5rem 3rem;
                position: relative;
                overflow: hidden;
            }}
            .coat-complete-inner::before {{
                content: "";
                position: absolute;
                top: -40px;
                left: 0;
                right: 0;
                height: 70px;
                background:
                    radial-gradient(circle at 10% 0, #ff1e1e80 0, transparent 55%),
                    radial-gradient(circle at 40% 0, #ff1e1ea0 0, transparent 60%),
                    radial-gradient(circle at 80% 0, #ff1e1e90 0, transparent 55%);
                pointer-events: none;
            }}
            .coat-complete-title {{
                font-family: "Cinzel", serif;
                font-size: 3rem;
                text-align: center;
                letter-spacing: 0.32em;
                text-transform: uppercase;
                color: #d4af37;
                text-shadow:
                    0 0 16px rgba(212, 175, 55, 0.9),
                    0 0 28px rgba(255, 255, 255, 0.8);
                margin-bottom: 1.2rem;
            }}
            .coat-complete-subtitle {{
                font-family: "Playfair Display", serif;
                text-align: center;
                color: #ff1e1e;
                font-size: 1.2rem;
                letter-spacing: 0.24em;
                text-transform: uppercase;
                margin-bottom: 1.8rem;
            }}
            .coat-complete-text {{
                font-family: "Georgia", serif;
                font-size: 1.1rem;
                line-height: 1.85;
                color: #f9f9f9;
            }}
            </style>
            <div class="coat-complete-overlay">
                <div class="coat-complete-inner">
                    <div class="coat-complete-title">
                        THE COAT IS FINISHED
                    </div>
                    <div class="coat-complete-subtitle">
                        CRUELLA IS COMPLETE. THE WORLD IS HER RUNWAY.
                    </div>
                    <div class="coat-complete-text">
                        {cruella_final}
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    time.sleep(5.0)
    st.rerun()


if __name__ == "__main__":
    main()
