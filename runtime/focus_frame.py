from __future__ import annotations

import json

from runtime.types import EvidenceCard, FocusFrame, TaskRequest


class FocusFrameManager:
    def build(
        self,
        task: TaskRequest,
        candidate_cards: list[EvidenceCard],
        quota_chars: int,
    ) -> FocusFrame:
        admitted: list[EvidenceCard] = []
        used_chars = 0

        for card in candidate_cards:
            payload = json.dumps(card.content, sort_keys=True)
            cost = len(payload)
            if used_chars + cost <= quota_chars:
                admitted.append(card)
                used_chars += cost

        delta_frame = {
            "query": task.query,
            "expected_fields": task.expected_fields,
        }

        return FocusFrame(
            task_id=task.task_id,
            agent_id=task.agent_id,
            prefix=task.prefix,
            goal=task.goal,
            admitted_cards=admitted,
            quota_chars=quota_chars,
            used_chars=used_chars,
            delta_frame=delta_frame,
        )