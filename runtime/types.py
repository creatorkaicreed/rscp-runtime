from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvidenceCard:
    card_id: str
    namespace: str
    card_type: str
    topic: str
    content: dict[str, Any]
    verification_status: str
    created_at: str

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "EvidenceCard":
        return cls(
            card_id=str(data["card_id"]),
            namespace=str(data.get("namespace", "default")),
            card_type=str(data.get("type", "fact")),
            topic=str(data.get("topic", "general")),
            content=dict(data.get("content", {})),
            verification_status=str(data.get("verification_status", "unknown")),
            created_at=str(data.get("created_at", "")),
        )


@dataclass
class TaskRequest:
    task_id: str
    agent_id: str
    namespace: str
    goal: str
    prefix: str
    query: str
    expected_fields: dict[str, Any] = field(default_factory=dict)


@dataclass
class FocusFrame:
    task_id: str
    agent_id: str
    prefix: str
    goal: str
    admitted_cards: list[EvidenceCard]
    quota_chars: int
    used_chars: int
    delta_frame: dict[str, Any]

    @property
    def admitted_card_ids(self) -> list[str]:
        return [card.card_id for card in self.admitted_cards]


@dataclass
class DraftOutput:
    task_id: str
    prefix: str
    fields: dict[str, Any]
    raw_text: str


@dataclass
class VerificationResult:
    task_id: str
    is_verified: bool
    mismatches: list[str]
    corrected_fields: dict[str, Any]


@dataclass
class RuntimeResult:
    task_id: str
    worker_id: int
    prefix: str
    prefix_cache_hit: bool
    focus_frame_chars: int
    admitted_cards: int
    verification_passed: bool
    output_fields: dict[str, Any]