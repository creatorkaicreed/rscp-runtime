import random
import time
from collections import Counter

WORKERS = 6
AGENTS = 50
FOCUS_FRAME_TARGET = 380

PREFIXES = [
    "policy_check",
    "compliance_review",
    "risk_assessment",
    "claims_verification",
]

CARDS = [
    "transaction_data",
    "policy_rule",
    "customer_history",
    "claim_record",
]


def run_simulation() -> None:
    print("RSCP Multi-Agent Simulation")
    print(f"Focus Frame Target: ~{FOCUS_FRAME_TARGET} chars")
    print("=" * 72)

    prefix_cache: set[str] = set()
    prefix_counter: Counter[str] = Counter()
    cache_hits = 0
    cache_misses = 0

    for agent in range(AGENTS):
        worker = (agent % WORKERS) + 1
        prefix = random.choice(PREFIXES)
        card = random.choice(CARDS)

        focus_chars = random.randint(374, 389)

        cache_hit = prefix in prefix_cache
        if cache_hit:
            cache_hits += 1
            cache_status = "CACHE HIT"
        else:
            cache_misses += 1
            cache_status = "CACHE MISS"
            prefix_cache.add(prefix)

        prefix_counter[prefix] += 1

        print(
            f"Agent {agent:02d} | "
            f"Worker {worker} | "
            f"Prefix {prefix} | "
            f"Card {card} | "
            f"Focus ~{focus_chars} chars | "
            f"{cache_status}"
        )

        time.sleep(0.05)

    print("\nSimulation complete.")
    print("=" * 72)
    print("Runtime Summary")
    print(f"Agents: {AGENTS}")
    print(f"Workers: {WORKERS}")
    print(f"Distinct Prefix Programs: {len(prefix_cache)}")
    print(f"Prefix Cache Hits: {cache_hits}")
    print(f"Prefix Cache Misses: {cache_misses}")
    print(f"Focus Frame Target: ~{FOCUS_FRAME_TARGET} chars")
    print("Evidence Source: external vault")
    print("Reasoning Envelope: bounded")

    print("\nPrefix Distribution")
    print("-" * 72)
    for prefix, count in prefix_counter.most_common():
        print(f"{prefix:<22} {count:>3}")


if __name__ == "__main__":
    run_simulation()