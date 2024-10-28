</code>

---

#### `tests/test_agent_manager.py`
Unit test for the `AgentManager` class.

<code>
```python
# tests/test_agent_manager.py
import unittest
from agent_framework.agent import Agent
from agent_framework.agent_manager import AgentManager
from agent_framework.task import Task

class TestAgentManager(unittest.TestCase):
    def test_add_and_send_message(self):
        manager = AgentManager()
        agent1 = Agent("Agent1")
        agent2 = Agent("Agent2")
        manager.add_agent(agent1)
        manager.add_agent(agent2)
        manager.send_message("Agent1", "Agent2", "Hello, Agent2!")
        # Check console output for expected behavior

if __name__ == "__main__":
    unittest.main()
