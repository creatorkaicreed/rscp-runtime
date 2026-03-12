README.md
# RSCP Runtime
### Bounded Reasoning Memory for Scalable Multi-Agent AI

RSCP (Reasoning-Scoped Context Protocol) is a reference prototype demonstrating how AI systems can operate with **bounded active reasoning** while retrieving knowledge from large external stores.

The prototype shows how reasoning context can remain constant even as stored knowledge grows — preventing the common **prompt explosion problem** seen in many AI pipelines.
<img width="2365" height="1514" alt="prompt_vs_rscp" src="https://github.com/user-attachments/assets/7e067a2f-a4d8-4304-bb0e-1fc7496e2692" />

---

## The Problem

Most AI systems scale knowledge by adding more context into the prompt.

As knowledge grows:

- prompt size increases
- latency increases
- memory usage increases
- token cost increases

This creates **prompt explosion**, where reasoning context grows linearly (or worse) with stored knowledge.

---

## The RSCP Idea

RSCP separates:

**Active Reasoning**  
from  
**Stored Knowledge**

Instead of loading all information into the prompt, the system:

1. selects a **reasoning prefix program**
2. retrieves a small **evidence card**
3. constructs a bounded **focus frame**

The reasoning envelope remains **constant size**.


Vault → Librarian → Evidence Card → Focus Frame → Reasoning


This prototype demonstrates the control-plane architecture required to support this model.

---

## Repository Structure


runtime/
focus_frame.py
prefix_cache.py
librarian.py
oracle.py
vault.py

demo/
run_demo.py
multi_agent_sim.py
benchmark_prompt_vs_rscp.py
benchmark_vault_growth.py
plot_prompt_vs_rscp.py

outputs/
benchmark_prompt_vs_rscp.csv
benchmark_vault_growth.csv

WhitePaper/
RSCP White Paper.pdf

config.py
main.py
run_all_demos.py
requirements.txt


---

## Core Components

### Vault
Stores knowledge cards (external evidence storage).

### Librarian
Selects the correct evidence card for a reasoning task.

### Prefix Cache
Stores reusable reasoning programs.

### Focus Frame
Constructs the bounded reasoning context.

### Oracle
Verifies reasoning determinism.

---

Vault
   ↓
Librarian
   ↓
Prefix Cache
   ↓
Focus Frame
   ↓
Reasoning Envelope

## Demo Modes

### 1. Basic Demo


python demo/run_demo.py


Runs a deterministic reasoning pipeline with evidence retrieval.

---

### 2. Multi-Agent Simulation


python demo/multi_agent_sim.py


Simulates many agents executing reasoning tasks while sharing prefix programs.

Example output:


Agent 42 | Worker 3 | Prefix policy_check | Card customer_history | Focus ~380 chars | CACHE HIT


---

### 3. Benchmark – Prompt Explosion


python demo/benchmark_prompt_vs_rscp.py


Compares naive prompt context with RSCP bounded reasoning.

Results are written to:


outputs/benchmark_prompt_vs_rscp.csv


---

### 4. Vault Growth Benchmark


python demo/benchmark_vault_growth.py


Tests how reasoning context scales as the knowledge vault grows.

---

### 5. Plot Results


python demo/plot_prompt_vs_rscp.py


Generates the comparison graph:

**Prompt Explosion vs Bounded Reasoning**

---

## Example Result

As vault size grows:

| Vault Size | Naive Prompt | RSCP |
|-------------|-------------|------|
| 100 | 1,270 chars | ~380 chars |
| 1,000 | 12,790 chars | ~380 chars |
| 10,000 | 128,890 chars | ~380 chars |

This demonstrates the **constant reasoning envelope** property.

---

## Why This Matters

Bounded reasoning architectures could enable:

- scalable multi-agent AI systems
- lower inference cost
- reduced latency
- deterministic reasoning pipelines
- large external knowledge stores without prompt explosion

---

## Status

This repository is a **research prototype** demonstrating the RSCP control-plane architecture.

It is not yet integrated with a production LLM runtime.

---

## License

Apache 2.0

Author

Graeme Randle
RusticLabs

How to run
Run it from the repo root with:
use:

python main.py

And for the full showcase:

python run_all_demos.py
