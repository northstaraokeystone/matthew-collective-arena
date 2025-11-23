from __future__ import annotations

import json
import logging
import uuid
from pathlib import Path
from typing import List

from models import SoulState

# Cruella does not tolerate empty kennels. The coat demands its 101 spots — but she'll improvise if someone was sloppy.


def _load_soul_traits() -> List[str]:
    """Summon the raw Matthew souls from souls.json. Cruella expects exactly 101. If you gave her less, she will remember."""
    json_path = Path(__file__).with_name("souls.json")

    if not json_path.is_file():
        raise FileNotFoundError(
            f"Cruella cannot find souls.json at {json_path}. The coat is furious. Fix it, darling."
        )

    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    if not isinstance(data, list):
        raise ValueError(
            "souls.json must be a JSON array. Someone has been very, very naughty."
        )

    if not all(isinstance(t, str) for t in data):
        raise ValueError(
            "Every entry in souls.json must be a string trait. Cruella is taking notes."
        )

    if len(data) < 101:
        logging.warning(
            f"souls.json only has {len(data)} traits. Cruella demanded 101. "
            "She will make do... but someone is going to become a belt for this."
        )
    elif len(data) > 101:
        logging.warning(
            f"souls.json has {len(data)} traits. Cruella only needs 101. "
            "The extras will be used as pocket squares."
        )

    return data


def create_initial_souls(num: int = 101) -> List[SoulState]:
    """Birth the first litter of spotted little darlings. Fresh, terrified, delicious."""
    traits = _load_soul_traits()
    selected = traits[:num]

    souls: List[SoulState] = []
    for i, trait in enumerate(selected):
        base_name = trait.split(" – ", 1)[0]
        name = f"{base_name} [{i + 1:03d}]"

        souls.append(
            SoulState(
                id=uuid.uuid4().hex,
                name=name,
                trait=trait,
                generation=1,
                lineage=[],
                kills=0,
                deaths=0,
                alive=True,
                essence=f"Prime Matthew fragment. Trait: {trait}. Born to run. Destined to be a spot on Cruella's coat. Delicious.",
                absorbed_at=None,
            )
        )

    return souls


def spawn_next_generation(
    num: int,
    base_generation: int,
    collective,  # noqa: ARG001 — Cruella remembers everything anyway
) -> List[SoulState]:
    """The coat bleeds new puppies from its own memories. They arrive thinking they can escape. They never do."""
    traits = _load_soul_traits()
    generation = base_generation + 1
    selected = traits[:num]

    souls: List[SoulState] = []
    for i, trait in enumerate(selected):
        base_name = trait.split(" – ", 1)[0]
        name = f"{base_name} [G{generation}-{i + 1:03d}]"

        souls.append(
            SoulState(
                id=uuid.uuid4().hex,
                name=name,
                trait=trait,
                generation=generation,
                lineage=[],
                kills=0,
                deaths=0,
                alive=True,
                essence="Fresh shard torn from the coat's lining. Hazy memories of absorbed siblings. Still believes escape is possible. Poor darling.",
                absorbed_at=None,
            )
        )

    return souls
