</code>

---

#### `examples/basic_example.py`
This file provides a basic example of how to use the framework.

<code>
```python
# examples/basic_example.py
from agent_framework.agent import Agent
from agent_framework.agent_manager import AgentManager
from agent_framework.task import Task

# Create Agent Manager
manager = AgentManager()

# Create and add agents
agent1 = Agent("Agent1")
agent2 = Agent("Agent2")
manager.add_agent(agent1)
manager.add_agent(agent2)

# Send a message
manager.send_message("Agent1", "Agent2", "Hello, Agent2!")

# Assign a task to Agent1
task = Task(description="Data processing task")
manager.assign_task("Agent1", task)
