from __future__ import annotations

import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DEMO_DIR = ROOT / "demo"
OUTPUTS_DIR = ROOT / "outputs"


def run_step(title: str, script_path: Path) -> bool:
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)

    if not script_path.exists():
        print(f"SKIP: {script_path} not found")
        return False

    result = subprocess.run(
        [sys.executable, str(script_path)],
        cwd=ROOT,
        text=True,
    )

    if result.returncode != 0:
        print(f"FAILED: {script_path.name} returned exit code {result.returncode}")
        return False

    print(f"OK: {script_path.name}")
    return True


def main() -> None:
    print("RSCP Demo Runner")
    print(f"Project Root: {ROOT}")

    OUTPUTS_DIR.mkdir(exist_ok=True)

    steps = [
        ("1. Live RSCP Runtime Demo", DEMO_DIR / "run_demo.py"),
        ("2. Multi-Agent Simulation", DEMO_DIR / "multi_agent_sim.py"),
        ("3. Prompt Explosion vs RSCP Benchmark", DEMO_DIR / "benchmark_prompt_vs_rscp.py"),
        ("4. Vault Growth Benchmark", DEMO_DIR / "benchmark_vault_growth.py"),
        ("5. Plot Prompt Explosion vs RSCP", DEMO_DIR / "plot_prompt_vs_rscp.py"),
    ]

    results: list[tuple[str, bool]] = []
    for title, script in steps:
        ok = run_step(title, script)
        results.append((title, ok))

    print("\n" + "=" * 80)
    print("RSCP Demo Runner Summary")
    print("=" * 80)

    for title, ok in results:
        status = "OK" if ok else "SKIPPED / FAILED"
        print(f"{status:16} {title}")

    print("\nDone.")
    print("If the plotting script exists, check the outputs/ folder for saved figures.")


if __name__ == "__main__":
    main()