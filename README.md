RSCP Runtime (Reference Prototype)

This repository contains a minimal reference implementation of the Reasoning State Control Plane (RSCP) runtime architecture.

RSCP introduces a new way to manage reasoning memory in AI systems by separating active reasoning state from external knowledge storage.

Instead of expanding prompt context indefinitely, RSCP maintains a bounded reasoning envelope and retrieves only the evidence required for each reasoning step.

This converts reasoning memory into a managed runtime resource, similar to how operating systems manage process memory.

Core Concepts

RSCP runtime executes reasoning tasks using four core components:

Bounded Reasoning Envelope (L1)

Active reasoning state is constrained to a fixed focus frame.

Example:

Focus Frame Size: ~380 chars

This prevents prompt context explosion as knowledge grows.

Evidence Vault (L2)

External knowledge is stored outside the reasoning envelope and admitted only when required.

Example runtime output:

Evidence Card Loaded: transaction_data
Vault Source: evidence_vault
Prefix Programs

Reasoning tasks reuse structured reasoning programs.

Example prefixes:

policy_check
compliance_review
risk_assessment
claims_verification

Prefix reuse enables high cache locality and improves multi-agent throughput.

Deterministic Verification

Each reasoning step may optionally pass through a verification layer.

Example:

Oracle Verification: OK
Example Runtime Output
TASK 22
Worker: 2
Reasoning Envelope: [bounded]
Reasoning Prefix: policy_check
Evidence Card Loaded: customer_history
Vault Source: evidence_vault
Focus Frame Size: 378 chars
PREFIX CACHE HIT
Oracle Verification: OK
Prompt Explosion vs RSCP

Runtime experiments demonstrate the difference between traditional prompt accumulation and RSCP bounded reasoning.

Vault Size	Naive Latency	Naive Context	RSCP Latency	RSCP Context
100	0.0539s	1,270 chars	0.0565s	381 chars
1000	0.2848s	12,790 chars	0.0569s	383 chars
10000	2.6099s	128,890 chars	0.0594s	383 chars

Key observation:

Naive prompt context grows with stored knowledge.
RSCP reasoning context remains bounded while latency stays nearly constant.

Running the Demo

Install dependencies:

python -m pip install -r requirements.txt

Run the demo:

python demo/run_demo.py
White Paper

The architecture is described in the RSCP white paper:

RSCP — Bounded Reasoning Memory for Scalable Multi-Agent AI Systems

Research Goal

RSCP explores a new runtime model where reasoning memory is treated as a first-class system resource, enabling:

• higher multi-agent density
• stable inference latency
• scalable knowledge vaults
• reliable reasoning pipelines

Multi-Agent Runtime Simulation

RSCP allows many agents to operate concurrently while maintaining bounded reasoning memory.

Example simulation output:

Agent 07 | Worker 2 | Prefix compliance_review | Card policy_rule | Focus ~380 chars
Agent 08 | Worker 3 | Prefix risk_assessment | Card customer_history | Focus ~380 chars
Agent 09 | Worker 4 | Prefix risk_assessment | Card customer_history | Focus ~380 chars

Agent 22 | Worker 5 | Prefix claims_verification | Card transaction_data | Focus ~378 chars | CACHE HIT
Agent 23 | Worker 6 | Prefix policy_check | Card customer_history | Focus ~386 chars | CACHE HIT
Agent 24 | Worker 1 | Prefix compliance_review | Card transaction_data | Focus ~374 chars | CACHE HIT

Simulation summary:

Agents: 50
Workers: 6
Distinct Prefix Programs: 4
Prefix Cache Hit Rate: 92%
Focus Frame Target: ~380 chars
Evidence Source: external vault
Reasoning Envelope: bounded

Even as agent count increases, the active reasoning context remains constant.

Status

This repository currently contains a minimal prototype runtime used for architectural exploration.

Future work includes:

• concurrent worker scheduling
• GPU-aware prefix caching
• distributed vault systems
• edge-runtime deployments

Author

Graeme Randle
RusticLabs
Patent Pending

How to run
Run it from the repo root with:
use:

python main.py

And for the full showcase:

python run_all_demos.py