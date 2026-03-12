from __future__ import annotations

from dataclasses import dataclass
from typing import Dict


@dataclass
class PrefixProgram:
    name: str
    description: str
    usage_count: int = 0


class PrefixLibrarian:
    def __init__(self) -> None:
        self.programs: Dict[str, PrefixProgram] = {}

    def register(self, name: str, description: str) -> None:
        if name not in self.programs:
            self.programs[name] = PrefixProgram(
                name=name,
                description=description,
            )

    def acquire(self, name: str) -> PrefixProgram:
        if name not in self.programs:
            raise ValueError(f"Prefix program not registered: {name}")

        program = self.programs[name]
        program.usage_count += 1
        return program

    def stats(self) -> dict[str, int]:
        return {name: program.usage_count for name, program in self.programs.items()}