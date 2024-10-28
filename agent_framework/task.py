</code>

---

#### `agent_framework/message.py`
This module defines the `Message` class, which allows agents to communicate.

<code>
```python
# agent_framework/message.py
class Message:
    def __init__(self, sender: str, recipient: str, content: str):
        self.sender = sender
        self.recipient = recipient
        self.content = content
