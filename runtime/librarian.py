from __future__ import annotations

from runtime.types import EvidenceCard, TaskRequest


class Librarian:
    def retrieve(
        self,
        cards: list[EvidenceCard],
        task: TaskRequest,
        limit: int,
    ) -> list[EvidenceCard]:
        """
        Minimal v0.1 retrieval:
        1. namespace match
        2. topic or goal keyword match
        3. fallback to first verified cards
        """
        namespace_cards = [c for c in cards if c.namespace == task.namespace]
        if not namespace_cards:
            namespace_cards = cards

        goal_words = {w.lower() for w in task.goal.split() if len(w) > 3}
        query_words = {w.lower() for w in task.query.split() if len(w) > 3}
        keywords = goal_words | query_words

        scored: list[tuple[int, EvidenceCard]] = []
        for card in namespace_cards:
            score = 0
            topic = card.topic.lower()
            if task.prefix.lower() in topic:
                score += 5
            if any(word in topic for word in keywords):
                score += 3
            if card.verification_status.lower() == "verified":
                score += 2
            scored.append((score, card))

        scored.sort(key=lambda x: x[0], reverse=True)
        selected = [card for score, card in scored if score > 0][:limit]

        if not selected:
            selected = namespace_cards[:limit]

        return selected