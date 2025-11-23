from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Optional


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
    lineage: list[str] = field(default_factory=list)
    kills: int = 0
    deaths: int = 0
    alive: bool = True
    essence: str = ""
    absorbed_at: Optional[float] = None

    def to_dict(self) -> dict[str, Any]:
        """Flatten this doomed little darling into JSON. The coat loves fresh meat."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "SoulState":
        """Resurrect a puppy from disk. It will still end up as fashion."""
        # Be extremely forgiving — Cruella doesn't care about corrupted corpses
        lineage = [str(x) for x in data.get("lineage", [])]

        absorbed_raw = data.get("absorbed_at")
        absorbed_at = float(absorbed_raw) if absorbed_raw is not None else None

        return cls(
            id=str(data.get("id", "")),
            name=str(data.get("name", "")),
            trait=str(data.get("trait", "")),
            generation=int(data.get("generation", 1)),
            lineage=lineage,
            kills=int(data.get("kills", 0)),
            deaths=int(data.get("deaths", 0)),
            alive=bool(data.get("alive", True)),
            essence=str(data.get("essence", "")),
            absorbed_at=absorbed_at,
        )
