from __future__ import annotations


class PrefixCache:
    def __init__(self) -> None:
        self._seen_prefixes: set[str] = set()

    def check_and_mark(self, prefix: str) -> bool:
        hit = prefix in self._seen_prefixes
        self._seen_prefixes.add(prefix)
        return hit

    def size(self) -> int:
        return len(self._seen_prefixes)