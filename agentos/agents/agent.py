from dataclasses import dataclass


@dataclass
class Agent:
    agent_id: str
    role: str
    current_task: str | None = None
    status: str = "idle"

    def assign_task(self, task: str):
        self.current_task = task
        self.status = "running"

    def complete_task(self):
        self.status = "idle"
        self.current_task = None

    def send_task(self, bus, target_id: str, task: str):
        bus.send(self.agent_id, target_id, task)