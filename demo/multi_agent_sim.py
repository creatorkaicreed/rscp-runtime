from __future__ import annotations

import argparse
import os
import random
import sys
from collections import Counter

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from runtime.prefix_librarian import PrefixLibrarian
from runtime.scheduler import RuntimeScheduler, ScheduledTask


DEFAULT_WORKERS = 6
DEFAULT_AGENTS = 50
DEFAULT_FOCUS_FRAME_TARGET = 380

PREFIXES = [
    ("policy_check", "Insurance policy validation"),
    ("compliance_review", "Regulatory compliance audit"),
    ("risk_assessment", "Risk evaluation logic"),
    ("claims_verification", "Claims processing verification"),
]

CARDS = [
    "transaction_data",
    "policy_rule",
    "customer_history",
    "claim_record",
]


def build_tasks(agent_count: int, librarian: PrefixLibrarian) -> tuple[list[ScheduledTask], Counter[str]]:
    tasks: list[ScheduledTask] = []
    prefix_counter: Counter[str] = Counter()

    for agent in range(agent_count):
        prefix_name, _ = random.choice(PREFIXES)
        card = random.choice(CARDS)

        # Acquire the reasoning program from the librarian
        librarian.acquire(prefix_name)

        tasks.append(
            ScheduledTask(
                agent_id=agent,
                prefix=prefix_name,
                card=card,
            )
        )
        prefix_counter[prefix_name] += 1

    return tasks, prefix_counter


def run_simulation(agent_count: int, worker_count: int, focus_frame_target: int) -> None:
    print("RSCP Multi-Agent Simulation")
    print(f"Agents: {agent_count}")
    print(f"Workers: {worker_count}")
    print(f"Focus Frame Target: ~{focus_frame_target} chars")
    print("=" * 88)

    librarian = PrefixLibrarian()
    for name, desc in PREFIXES:
        librarian.register(name, desc)

    tasks, prefix_counter = build_tasks(agent_count, librarian)

    scheduler = RuntimeScheduler(
        worker_count=worker_count,
        focus_frame_target=focus_frame_target,
    )

    scheduler.submit_tasks(tasks)
    scheduler.run()

    stats = scheduler.summary()

    print("\nSimulation complete.")
    print("=" * 88)
    print("Runtime Summary")
    print(f"Runtime Seconds: {stats['runtime_seconds']}")
    print(f"Simulated Tasks / Second: {stats['tasks_per_second']}")
    print(f"Agents: {agent_count}")
    print(f"Workers: {stats['workers']}")
    print(f"Completed Tasks: {stats['completed_tasks']}")
    print(f"Distinct Prefix Programs: {stats['distinct_prefixes']}")
    print(f"Prefix Cache Hits: {stats['cache_hits']}")
    print(f"Prefix Cache Misses: {stats['cache_misses']}")
    print(f"Prefix Cache Hit Rate: {stats['cache_hit_rate_pct']}%")
    print(f"Focus Frame Target: ~{stats['focus_frame_target']} chars")
    print("Evidence Source: external vault")
    print("Reasoning Envelope: bounded")

    print("\nPrefix Distribution")
    print("-" * 88)
    for prefix, count in prefix_counter.most_common():
        print(f"{prefix:<22} {count:>4}")

    print("\nPrefix Librarian Usage")
    print("-" * 88)
    for name, count in librarian.stats().items():
        print(f"{name:<22} {count:>4}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="RSCP multi-agent runtime simulation")
    parser.add_argument("--agents", type=int, default=DEFAULT_AGENTS, help="Number of agents/tasks to simulate")
    parser.add_argument("--workers", type=int, default=DEFAULT_WORKERS, help="Number of worker threads")
    parser.add_argument(
        "--focus",
        type=int,
        default=DEFAULT_FOCUS_FRAME_TARGET,
        help="Target focus frame size in chars",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_simulation(
        agent_count=args.agents,
        worker_count=args.workers,
        focus_frame_target=args.focus,
    )