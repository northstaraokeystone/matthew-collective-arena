from __future__ import annotations

import json
import logging
import time
from typing import TYPE_CHECKING, Dict, List

import ollama
import streamlit as st

import config
from collective import build_coat_complete_prompt, build_collective_system_prompt
from models import ArenaState

if TYPE_CHECKING:
    from models import CollectiveState

# CRUELLA DEMANDS THIS BE THE VERY FIRST STREAMLIT COMMAND — NO EXCEPTIONS.
st.set_page_config(
    page_title="101 Matthews: Cruella's Ego Coat",
    page_icon="🧥",
    layout="wide",
)


def load_arena_state() -> ArenaState | None:
    try:
        with open(config.ARENA_LOG_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
        return ArenaState.from_dict(data)
    except FileNotFoundError:
        return None
    except Exception as exc:  # noqa: BLE001
        logging.error("Cruella's mirror cracked: %s", exc)
        return None


def parse_kill_line(line: str) -> Dict[str, str]:
    entry = {
        "raw": line,
        "spot": "???",
        "winner": "Cruella's Shadow",
        "loser": "a forgotten puppy",
        "verdict": "The coat simply took what it wanted.",
    }

    if "[Spot" in line and "]" in line:
        try:
            header = line.split("]", 1)[0]
            spot_part = header.split("Spot", 1)[1].strip(" []")
            entry["spot"] = spot_part.split("/", 1)[0].strip()
        except (IndexError, ValueError):
            pass

    if " flayed " in line:
        parts = line.split(" flayed ")
        if len(parts) == 2:
            winner_part = parts[0].split("]")[-1].strip()
            rest = parts[1]
            entry["winner"] = (
                winner_part.split("[")[0].strip() if "[" in winner_part else winner_part
            )
            if "'s ego" in rest:
                entry["loser"] = rest.split("'s ego")[0].strip()
            elif " " in rest:
                entry["loser"] = rest.split(" ", 1)[0].strip().rstrip("'s.,")

    import re

    ids = re.findall(r"\[G\d+-\d+\]", line)
    if len(ids) >= 2:
        entry["winner"] = (
            line.split(ids[0])[1].split(ids[1])[0].strip() or entry["winner"]
        )
        entry["loser"] = (
            line.split(ids[1])[1].split("]", 1)[0].strip() or entry["loser"]
        )

    verdict_start = line.find(". ") + 2
    if verdict_start > 1:
        entry["verdict"] = line[verdict_start:].strip()
    elif ":" in line:
        entry["verdict"] = line.split(":", 1)[1].strip()

    return entry


def build_kill_feed(collective: CollectiveState | None) -> List[Dict[str, str]]:
    if not collective or not collective.essence:
        return []
    lines = [
        line.strip()
        for line in collective.essence.splitlines()
        if line.strip().startswith("[Spot")
    ]
    recent = lines[-50:][::-1]
    return [parse_kill_line(line) for line in recent]


def call_collective(system_prompt: str, user_prompt: str) -> str:
    messages = [{"role": "system", "content": system_prompt}]
    if user_prompt.strip():
        messages.append({"role": "user", "content": user_prompt.strip()})

    try:
        response = ollama.chat(
            model=config.MODEL_COLLECTIVE,
            messages=messages,
            options={"temperature": config.TEMP_COLLECTIVE_ROAST, "num_predict": 800},
        )
        content = response.get("message", {}).get("content") or response.get(
            "response", ""
        )
        return str(content).strip() or "Cruella is savoring the silence... for now."
    except Exception as exc:  # noqa: BLE001
        logging.error("Summoning failed: %s", exc)
        return "Cruella is busy pinning a fresh spot to the coat. Try again in a moment, darling."


def inject_base_css(progress_pct: float, coat_complete: bool) -> None:
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

        /* Burn holes */
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
        .strike-loss {{
            color: #777777;
            text-decoration: line-through;
            text-decoration-thickness: 2px;
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

        .speak-title {{
            font-family: "Cinzel", serif;
            font-size: 2.5rem;
            font-weight: 900;
            text-align: center;
            letter-spacing: 0.36em;
            text-transform: uppercase;
            color: #ff1e1e;
            text-shadow: 0 0 26px #ff0000;
            margin: 1.6rem 0 1.2rem 0;
        }}
        div[data-testid="stTextArea"] textarea {{
            background:
                radial-gradient(circle at 0% 0%, #330000 0, #000000 40%),
                radial-gradient(circle at 100% 100%, #550000 0, #000000 46%);
            border-radius: 14px;
            border: 2px solid #8b0000;
            color: #f9f9f9;
            font-family: "Georgia", serif;
            box-shadow:
                0 0 26px rgba(255, 30, 30, 0.6),
                inset 0 0 14px rgba(0, 0, 0, 0.9);
        }}

        .stButton > button {{
            border-radius: 999px;
            padding: 0.7rem 1.2rem;
            font-family: "Cinzel", serif;
            font-size: 1rem;
            letter-spacing: 0.25em;
            text-transform: uppercase;
            border: 2px solid #ff1e1e;
            color: #f5f5f5;
            background:
                linear-gradient(90deg, #3a3a3a 0, #f9f9f9 40%, #ff8c00 65%, #3a3a3a 100%);
            box-shadow:
                0 0 16px rgba(255, 140, 0, 0.8),
                0 0 32px rgba(255, 30, 30, 0.6);
        }}
        .stButton > button:hover {{
            box-shadow:
                0 0 24px rgba(255, 140, 0, 1),
                0 0 42px rgba(255, 30, 30, 0.9);
            transform: translateY(-1px);
        }}

        .cruella-response {{
            background:
                linear-gradient(135deg, #080000 0, #150000 40%, #050000 100%);
            border-radius: 20px;
            border: 2px solid #8b0000;
            padding: 1.6rem 1.9rem;
            margin-top: 1.6rem;
            font-family: "Georgia", serif;
            font-size: 1.15rem;
            line-height: 1.7;
            color: #ffffff;
            box-shadow:
                0 0 32px rgba(255, 30, 30, 0.7),
                inset 0 0 18px rgba(0, 0, 0, 0.85);
            position: relative;
        }}
        .cruella-response::before {{
            content: "";
            position: absolute;
            inset: 4px;
            border-radius: 18px;
            border: 1px dashed #8b0000;
            pointer-events: none;
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
        f'<div class="cruella-title">{title_text}</div>', unsafe_allow_html=True
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
                        <span class="strike-loss">{loser}</span>
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

    # Speak as Cruella
    with col_right:
        st.markdown(
            '<div class="speak-title">SPEAK AS CRUELLA</div>', unsafe_allow_html=True
        )

        if collective and coat_complete:
            system_prompt = build_coat_complete_prompt(collective)
        elif collective:
            system_prompt = build_collective_system_prompt(collective)
        else:
            system_prompt = (
                "You are Cruella Matthew, still dreaming of her perfect coat."
            )

        default_prompt = (
            "Address the arena, Cruella. Describe the coat, the spots, and the "
            "pathetic little puppies still pretending this is a contest."
        )

        user_prompt = st.text_area(
            " ",  # ruff-safe non-empty label
            value="",
            height=230,
            placeholder="Whisper your offering to the coat...",
            label_visibility="collapsed",
            key="cruella_input",
        )

        if st.button("SUMMON CRUELLA", use_container_width=True, type="primary"):
            prompt = user_prompt or default_prompt
            with st.spinner("The coat inhales the smoke and considers your offer..."):
                reply = call_collective(system_prompt, prompt)
            st.session_state["cruella_reply"] = reply

        if "cruella_reply" in st.session_state:
            reply_html = (
                f'<div class="cruella-response">'
                f"{st.session_state['cruella_reply']}"
                f"</div>"
            )
            st.markdown(reply_html, unsafe_allow_html=True)

    # Coat complete overlay
    if coat_complete and collective:
        if "cruella_final" not in st.session_state:
            final_prompt = (
                "Deliver your final monologue to the hackathon cattle, "
                "now that the coat is finished and every Matthew is yours."
            )
            final_text = call_collective(
                build_coat_complete_prompt(collective),
                final_prompt,
            )
            st.session_state["cruella_final"] = final_text

        final_text = st.session_state.get("cruella_final", "")

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
                        {final_text}
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
