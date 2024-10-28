def add_agent(self, agent: Agent):
    self.agents[agent.name] = agent
    print(f"Agent {agent.name} added to the system.")

def send_message(self, sender_name: str, recipient_name: str, content: str):
    message = Message(sender_name, recipient_name, content)
    if recipient_name in self.agents:
        response = self.agents[recipient_name].process_message(message)
        print(f"Response from {recipient_name}: {response}")
    else:
        print(f"Agent {recipient_name} not found.")

def assign_task(self, agent_name: str, task: Task):
    if agent_name in self.agents:
        self.agents[agent_name].perform_task(task)
    else:
        print(f"Agent {agent_name} not found.")
