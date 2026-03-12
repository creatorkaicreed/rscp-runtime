from dataclasses import dataclass


@dataclass(frozen=True)
class RuntimeConfig:
    focus_frame_quota_chars: int = 800
    max_cards_per_task: int = 3
    worker_count: int = 6
    vault_root: str = "vault"
    default_namespace: str = "claims"
    default_model_name: str = "demo-model"


CONFIG = RuntimeConfig()