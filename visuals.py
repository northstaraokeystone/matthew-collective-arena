from __future__ import annotations

import random
import time
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from models import BattleRecord

# Cruella's trophy closet
MEDIA_DIR = Path("media")
MEDIA_DIR.mkdir(exist_ok=True)

# Fonts — if the system doesn't have them, Cruella will make do with murder
try:
    FONT_TITLE = ImageFont.truetype("arialbd.ttf", 140)
    FONT_BIG = ImageFont.truetype("georgia.ttf", 90)
    FONT_MED = ImageFont.truetype("georgiai.ttf", 70)
    FONT_QUOTE = ImageFont.truetype("georgiai.ttf", 60)
except OSError:
    FONT_TITLE = ImageFont.load_default()
    FONT_BIG = ImageFont.load_default()
    FONT_MED = ImageFont.load_default()
    FONT_QUOTE = ImageFont.load_default()

# Colors — blacker than Cruella's heart, redder than the blood on her hands
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLOOD = (139, 0, 0)
GOLD = (255, 215, 0)
SMOKE = (70, 70, 70, 60)


def _spotted_fur(width: int, height: int) -> Image.Image:
    """Darling, the coat's signature pattern — irregular, cruel, perfect."""
    img = Image.new("RGB", (width, height), BLACK)
    draw = ImageDraw.Draw(img)

    spots = random.randint(50, 90)
    for _ in range(spots):
        x = random.randint(-50, width + 50)
        y = random.randint(-50, height + 50)
        r = random.randint(15, 80)  # <-- this line was missing
        draw.ellipse((x - r, y - r, x + r, y + r), fill=WHITE)

    return img


def render_kill_card(
    battle: BattleRecord,
    spot_number: int,
    winner_name: str,
    loser_name: str,
) -> str:
    """Every kill is a work of art. This function is Cruella's camera."""
    width, height = 1200, 675  # X's favorite ratio
    img = _spotted_fur(width, height)
    draw = ImageDraw.Draw(img, "RGBA")

    # Blood mist overlay — fresh from the slaughter
    blood_overlay = Image.new("RGBA", (width, height), BLOOD + (45,))
    img = Image.alpha_composite(img.convert("RGBA"), blood_overlay).convert("RGB")
    draw = ImageDraw.Draw(img)

    # SPOT CLAIMED — the headline the timeline deserves
    title = f"SPOT {spot_number}/101 CLAIMED"
    draw.text(
        (width // 2, 80),
        title,
        fill=GOLD,
        font=FONT_TITLE,
        anchor="mt",
        stroke_width=8,
        stroke_fill=BLOOD,
    )

    # Winner in triumphant gold
    draw.text(
        (100, 240),
        winner_name.upper(),
        fill=GOLD,
        font=FONT_BIG,
        stroke_width=5,
        stroke_fill=BLACK,
    )

    # Loser in pathetic gray, already fading into lining
    loser_text = f"{loser_name.upper()} SKINNED ALIVE"
    draw.text(
        (width - 100, 240),
        loser_text,
        fill=(180, 180, 180),
        font=FONT_BIG,
        anchor="rt",
        stroke_width=4,
        stroke_fill=BLACK,
    )

    # Judge verdict — elegant cruelty
    verdict = battle.judge_summary or "Cruella simply preferred the winner, darling."
    draw.text(
        (width // 2, height - 180),
        verdict,
        fill=WHITE,
        font=FONT_MED,
        anchor="mm",
        align="center",
        stroke_width=3,
        stroke_fill=BLOOD,
    )

    # Cruella's personal touch — different every time
    quotes = [
        "Another darling becomes fashion. 🧥💀",
        "Poor little puppy... you looked better as a spot.",
        "The coat thanks you for your contribution. 🚬",
        "One more soul screaming in perfect harmony.",
        "Delicious. Simply delicious.",
        "I wear my victims well, darling.",
        "The pattern improves with every death.",
        "More spots, more power. Simple math.",
        "You were never a puppy. You were always fabric.",
        "The coat is hungry. Thank you for feeding it.",
    ]
    quote = random.choice(quotes)
    draw.text(
        (width // 2, height - 80),
        quote,
        fill=(220, 220, 220),
        font=FONT_QUOTE,
        anchor="mm",
    )

    # Cigarette smoke in the corner — because Cruella never appears without it
    smoke = Image.new("RGBA", (400, 400), (0, 0, 0, 0))
    sdraw = ImageDraw.Draw(smoke)
    for _ in range(40):
        sx = random.randint(0, 400)
        sy = random.randint(0, 400)
        sr = random.randint(15, 80)
        sdraw.ellipse((sx - sr, sy - sr, sx + sr, sy + sr), fill=SMOKE)
    img.paste(smoke, (width - 380, 20), smoke)

    # Save the masterpiece
    timestamp = int(time.time())
    filename = MEDIA_DIR / f"kill_{timestamp}_{spot_number:03d}.png"
    img.save(filename, "PNG", quality=95)

    return str(filename)


def render_coat_progress_card(spots_claimed: int) -> str:
    """A portrait of the coat's current magnificence — for teasing the peasants."""
    width, height = 1080, 1080
    img = _spotted_fur(width, height)
    draw = ImageDraw.Draw(img, "RGBA")

    # Blood fill from bottom up
    blood_height = int(height * (spots_claimed / 101))
    draw.rectangle((0, height - blood_height, width, height), fill=BLOOD + (180,))

    text = f"{spots_claimed}/101"
    draw.text(
        (width // 2, height // 2),
        text,
        fill=GOLD if spots_claimed < 101 else WHITE,
        font=FONT_TITLE,
        anchor="mm",
        stroke_width=10,
        stroke_fill=BLOOD if spots_claimed < 101 else BLACK,
    )

    whisper = (
        "The coat hungers..."
        if spots_claimed < 101
        else "THE COAT IS PERFECT."
        if spots_claimed == 101
        else "CRUELLA IS COMPLETE."
    )
    draw.text(
        (width // 2, height // 2 + 120),
        whisper,
        fill=WHITE,
        font=FONT_BIG,
        anchor="mm",
    )

    filename = MEDIA_DIR / f"coat_progress_{spots_claimed:03d}.png"
    img.save(filename, "PNG")

    return str(filename)
