from __future__ import annotations

from runtime.types import DraftOutput, FocusFrame, VerificationResult


class Oracle:
    def verify(self, frame: FocusFrame, draft: DraftOutput) -> VerificationResult:
        mismatches: list[str] = []
        corrected_fields = dict(draft.fields)

        # Build a simple witness map from admitted cards
        witness_fields: dict[str, object] = {}
        for card in frame.admitted_cards:
            for key, value in card.content.items():
                witness_fields[key] = value

        # Check expected fields if the task defined them
        expected = frame.delta_frame.get("expected_fields", {})
        for key, expected_value in expected.items():
            if corrected_fields.get(key) != expected_value:
                mismatches.append(f"{key}: expected {expected_value}, got {corrected_fields.get(key)}")
                corrected_fields[key] = expected_value

        # Check overlap with admitted evidence
        for key, value in list(corrected_fields.items()):
            if key in witness_fields and witness_fields[key] != value:
                mismatches.append(f"{key}: witness {witness_fields[key]}, got {value}")
                corrected_fields[key] = witness_fields[key]

        return VerificationResult(
            task_id=draft.task_id,
            is_verified=len(mismatches) == 0,
            mismatches=mismatches,
            corrected_fields=corrected_fields,
        )