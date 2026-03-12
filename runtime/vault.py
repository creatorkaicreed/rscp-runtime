from __future__ import annotations

import json
from pathlib import Path

from runtime.types import EvidenceCard


class EvidenceVault:
    def __init__(self, root_dir: str) -> None:
        self.root_dir = Path(root_dir)

    def load_cards_from_subdir(self, subdir: str) -> list[EvidenceCard]:
        target = self.root_dir / subdir
        if not target.exists():
            raise FileNotFoundError(f"Vault directory not found: {target}")

        cards: list[EvidenceCard] = []
        for path in sorted(target.glob("*.json")):
            with path.open("r", encoding="utf-8") as f:
                data = json.load(f)
            cards.append(EvidenceCard.from_dict(data))
        return cards