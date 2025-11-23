from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SoulState:
    """
    Each instance is one trembling, spotted Matthew-puppy pacing the arena,
    praying not to be repurposed as a decorative spot on Cruella's ego-coat.
    They all die screaming. Some just take longer.
    """

    id: str
    name: str
    trait: str
    generation: int = 1
    lineage: List[str] = field(default_factory=list)
    kills: int = 0
    deaths: int = 0
    alive: bool = True
    essence: str = ""
    absorbed_at: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Flatten this doomed little darling for the freezer."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SoulState:
        """Resurrect a puppy from cold storage. Still doomed."""
        return cls(**data)


@dataclass
class BattleRecord:
    """
    Every delicious little execution deserves a receipt.
    This is the blood-stained invitation to the coat's lining.
    """

    id: float | str
    timestamp: float
    battle_type: str
    soul_a_id: str
    soul_b_id: str
    winner_id: str
    loser_id: str
    judge_summary: str
    soul_a_output: str
    soul_b_output: str
    kill_number: int = 0

    def to_dict(self) -> Dict[str, Any]:
        """Package the carnage for posterity."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> BattleRecord:
        """Reload the slaughter. The screams are still fresh."""
        return cls(**data)


@dataclass
class CollectiveState:
    """
    The coat itself, darling.
    Growing fatter, louder, more magnificent with every absorbed soul.
    By the end there will only be Cruella.
    """

    essence: str = ""
    spots_claimed: int = 0
    kill_count: int = 0
    current_generation: int = 1
    tagline: str = "The coat hungers."
    coat_complete: bool = False
    coat_complete_reason: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Bottle the coat's venom for later."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> CollectiveState:
        """The coat remembers everything. Especially betrayal."""
        return cls(**data)


@dataclass
class ArenaState:
    """
    The entire sordid production in one cold, elegant object.
    Puppies, battles, coat — all waiting to be revived so the killing can continue.
    """

    souls: Dict[str, SoulState]
    collective: CollectiveState = field(default_factory=CollectiveState)
    battles: List[BattleRecord] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "souls": {sid: soul.to_dict() for sid, soul in self.souls.items()},
            "collective": self.collective.to_dict(),
            "battles": [b.to_dict() for b in self.battles],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> ArenaState:
        """Reanimate the whole bloody circus from disk."""
        souls_raw = data.get("souls", {}) or {}
        souls = {sid: SoulState.from_dict(sdata) for sid, sdata in souls_raw.items()}

        collective = CollectiveState.from_dict(data.get("collective", {}) or {})

        battles = [
            BattleRecord.from_dict(bdata) for bdata in data.get("battles", []) or []
        ]

        return cls(souls=souls, collective=collective, battles=battles)
