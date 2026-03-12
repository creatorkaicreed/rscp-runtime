class MessageBus:
    """
    Minimal in-memory message bus for agent-to-agent communication.
    """

    def __init__(self):
        self.messages = []

    def send(self, sender_id: str, target_id: str, task: str):
        self.messages.append({
            "sender": sender_id,
            "target": target_id,
            "task": task
        })

    def get_for_agent(self, agent_id: str):
        agent_messages = [m for m in self.messages if m["target"] == agent_id]
        self.messages = [m for m in self.messages if m["target"] != agent_id]
        return agent_messages