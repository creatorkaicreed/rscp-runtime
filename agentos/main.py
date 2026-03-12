from agents.agent import Agent
from governance.oracle import Oracle
from governance.governor import AdmissionController
from kernel.scheduler import KernelScheduler
from kernel.message_bus import MessageBus
from execution.simulation_executor import SimulationExecutor

from memory.prefix_librarian import PrefixLibrarian
from memory.prefix_cache import PrefixCache
from memory.focus_frame import FocusFrame
from memory.evidence_vault import EvidenceVault
from memory.agent_state import AgentStateStore


def main():

    print("AgentOS Runtime Booting")

    oracle = Oracle()
    admission = AdmissionController()
    executor = SimulationExecutor()
    scheduler = KernelScheduler()
    bus = MessageBus()

    librarian = PrefixLibrarian()
    focus = FocusFrame()
    cache = PrefixCache()
    vault = EvidenceVault()
    state = AgentStateStore()

    agents = {
        "agent_001": Agent("agent_001", "claims_agent"),
        "agent_002": Agent("agent_002", "compliance_agent"),
        "agent_003": Agent("agent_003", "risk_agent"),
    }

    # initialize state
    for agent in agents.values():
        state.init_agent(agent.agent_id)

    # agent_001 delegates work to other agents
    agents["agent_001"].send_task(bus, "agent_002", "Review compliance for claim CLM-1002")
    agents["agent_001"].send_task(bus, "agent_003", "Assess risk for claim CLM-1003")

    # agent_001 also keeps its own work
    local_tasks = [
        ("agent_001", "Verify claim CLM-1001"),
    ]

    # schedule local tasks
    for agent_id, task in local_tasks:
        agent = agents[agent_id]
        state.set_status(agent.agent_id, "running")

        program_name = "policy_check"

        if cache.has(program_name):
            program = cache.get(program_name)
            print(f"[PrefixCache] HIT: {program_name}")
        else:
            program = librarian.get_program(program_name)
            cache.store(program_name, program)
            print(f"[PrefixCache] MISS: {program_name}")

        claim_number = 1000 + int(agent.agent_id[-1])
        evidence_key = f"claim_record_{claim_number}"
        evidence = vault.retrieve(evidence_key)
        admitted = admission.admit(evidence)

        print(f"[Admission] Admitted fields: {list(admitted.keys())}")

        state.update(agent.agent_id, task=task, prefix=program)

        prompt = focus.build(program, task, admitted)
        scheduler.submit(agent, prompt)

    # schedule bus messages
    for agent_id, agent in agents.items():
        inbox = bus.get_for_agent(agent_id)

        for msg in inbox:
            state.set_status(agent.agent_id, "running")

            if agent.role == "compliance_agent":
                program_name = "compliance_review"
            elif agent.role == "risk_agent":
                program_name = "risk_assessment"
            else:
                program_name = "policy_check"

            if cache.has(program_name):
                program = cache.get(program_name)
                print(f"[PrefixCache] HIT: {program_name}")
            else:
                program = librarian.get_program(program_name)
                cache.store(program_name, program)
                print(f"[PrefixCache] MISS: {program_name}")

            claim_number = 1000 + int(agent.agent_id[-1])
            evidence_key = f"claim_record_{claim_number}"
            evidence = vault.retrieve(evidence_key)
            admitted = admission.admit(evidence)

            print(f"[Bus] {msg['sender']} -> {msg['target']} : {msg['task']}")
            print(f"[Admission] Admitted fields: {list(admitted.keys())}")

            state.update(agent.agent_id, task=msg["task"], prefix=program)

            prompt = focus.build(program, msg["task"], admitted)
            scheduler.submit(agent, prompt)

    # run scheduled work
    scheduler.run(executor, oracle)

    # finalize state
    for agent in agents.values():
        state.update(agent.agent_id, verified=True)
        state.set_status(agent.agent_id, "idle")
        print(f"[State] {agent.agent_id} -> {state.get(agent.agent_id)}")


if __name__ == "__main__":
    main()