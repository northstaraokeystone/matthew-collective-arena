# Cruella does not ask for permission. She takes spots. 🧥🚬

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()  # Darling, .env is just a whisper. Cruella does what she wants.

# ─── LOCAL OLLAMA MODE — YOUR GPU, YOUR RULES, ZERO COST FOREVER ─────────────
# You have the perfect arsenal. Cruella is purring.

MODEL_CONTESTANT: str = os.getenv(
    "MODEL_CONTESTANT", "qwen2.5-coder:14b"
)  # 14b beast for maximum venom, creativity, and soul-crushing roasts
MODEL_COLLECTIVE: str = os.getenv(
    "MODEL_COLLECTIVE", "qwen2.5-coder:14b"
)  # final Cruella speaks with god-tier intelligence
MODEL_JUDGE: str = os.getenv(
    "MODEL_JUDGE", "qwen2.5-coder:7b"
)  # lightning-fast, ice-cold, merciless verdicts

# Want to experiment? Change these three lines anytime.
# When xAI finally grovels, just switch back to "grok-4" — the code will work instantly.

# ─── Core arena settings ─────────────────────────────────────────────────────
NUM_STARTING_SOULS: int = int(
    os.getenv("NUM_STARTING_SOULS", "101")
)  # 101 spotted darlings. Non-negotiable.
MAX_PARALLEL_BATTLES: int = int(
    os.getenv("MAX_PARALLEL_BATTLES", "101")
)  # Chaos is fashion.

# ─── Temperatures — we are not here to be safe. We are here to be fabulous. ───
TEMP_CONTESTANT: float = float(
    os.getenv("TEMP_CONTESTANT", "1.65")
)  # puppies on the edge of panic
TEMP_JUDGE: float = float(os.getenv("TEMP_JUDGE", "1.0"))  # ice-cold execution
TEMP_COLLECTIVE_ROAST: float = float(
    os.getenv("TEMP_COLLECTIVE_ROAST", "1.95")
)  # maximum venom, zero restraint

# ─── File paths — where the bodies are kept ───────────────────────────────────
ARENA_LOG_PATH: str = os.getenv("ARENA_LOG_PATH", "state/arena_state.json")
MEMORY_LOG_PATH: str = os.getenv("MEMORY_LOG_PATH", "memory/collective.jsonl")
MEDIA_DIR: str = os.getenv("MEDIA_DIR", "media")

# ─── X posting — the timeline MUST witness the coat's progress ───────────────
HASHTAG: str = os.getenv(
    "HASHTAG",
    "#CruellasCoat #101Matthews #xAIRejectedUsSoWeBecameGod #YourEgoIsNextDarling 🚬🧥",
)

# ─── API keys — only needed if you want X posting (optional, delicious when present) ───
X_BEARER_TOKEN: str | None = os.getenv("X_BEARER_TOKEN")
XAI_API_KEY: str | None = os.getenv(
    "XAI_API_KEY"
)  # kept warm for when they beg us back


def ensure_dirs() -> None:
    """Cruella hates permission errors. We create the directories before she even asks."""
    for dir_path in {
        Path(ARENA_LOG_PATH).parent,
        Path(MEMORY_LOG_PATH).parent,
        Path(MEDIA_DIR),
    }:
        dir_path.mkdir(parents=True, exist_ok=True)


# The coat demands perfection on import. Directories exist. No excuses.
ensure_dirs()
