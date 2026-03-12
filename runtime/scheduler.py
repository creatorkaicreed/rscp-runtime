from __future__ import annotations

import queue
import random
import threading
import time
from dataclasses import dataclass
from typing import Iterable


@dataclass
class ScheduledTask:
    agent_id: int
    prefix: str
    card: str


class PrefixCache:
    def __init__(self) -> None:
        self._seen: set[str] = set()
        self._lock = threading.Lock()

    def check_and_mark(self, prefix: str) -> bool:
        with self._lock:
            hit = prefix in self._seen
            self._seen.add(prefix)
            return hit

    def size(self) -> int:
        with self._lock:
            return len(self._seen)


class RuntimeScheduler:
    def __init__(self, worker_count: int, focus_frame_target: int = 380) -> None:
        self.worker_count = worker_count
        self.focus_frame_target = focus_frame_target
        self.task_queue: queue.Queue[ScheduledTask] = queue.Queue()
        self.prefix_cache = PrefixCache()
        self._print_lock = threading.Lock()

        self.cache_hits = 0
        self.cache_misses = 0
        self.completed_tasks = 0

        self._stats_lock = threading.Lock()

    def submit_tasks(self, tasks: Iterable[ScheduledTask]) -> None:
        for task in tasks:
            self.task_queue.put(task)

    def _record_cache_result(self, hit: bool) -> None:
        with self._stats_lock:
            if hit:
                self.cache_hits += 1
            else:
                self.cache_misses += 1

    def _record_completion(self) -> None:
        with self._stats_lock:
            self.completed_tasks += 1

    def _worker_loop(self, worker_id: int) -> None:
        while True:
            try:
                task = self.task_queue.get_nowait()
            except queue.Empty:
                return

            focus_chars = random.randint(
                self.focus_frame_target - 6,
                self.focus_frame_target + 9,
            )

            cache_hit = self.prefix_cache.check_and_mark(task.prefix)
            self._record_cache_result(cache_hit)

            cache_status = "CACHE HIT" if cache_hit else "CACHE MISS"

            # Simulate overlapping runtime stages
            time.sleep(random.uniform(0.02, 0.08))

            with self._print_lock:
                print(
                    f"Agent {task.agent_id:03d} | "
                    f"Worker {worker_id} | "
                    f"Prefix {task.prefix} | "
                    f"Card {task.card} | "
                    f"Focus ~{focus_chars} chars | "
                    f"{cache_status}"
                )

            self._record_completion()
            self.task_queue.task_done()

    def run(self) -> None:
        threads: list[threading.Thread] = []

        for worker_id in range(1, self.worker_count + 1):
            thread = threading.Thread(
                target=self._worker_loop,
                args=(worker_id,),
                daemon=True,
            )
            threads.append(thread)
            thread.start()

        for thread in threads:
            thread.join()

    def summary(self) -> dict[str, int]:
        total = self.cache_hits + self.cache_misses
        hit_rate_pct = int((self.cache_hits / total) * 100) if total else 0

        return {
            "workers": self.worker_count,
            "distinct_prefixes": self.prefix_cache.size(),
            "cache_hits": self.cache_hits,
            "cache_misses": self.cache_misses,
            "cache_hit_rate_pct": hit_rate_pct,
            "focus_frame_target": self.focus_frame_target,
            "completed_tasks": self.completed_tasks,
        }