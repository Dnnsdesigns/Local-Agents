@staticmethod
def load_state(agent, file_path="agent_state.json"):
    try:
        with open(file_path, "r") as file:
            state = json.load(file)
            agent.name = state["name"]
            print(f"Agent state loaded from {file_path}.")
    except FileNotFoundError:
        print(f"No state file found at {file_path}.")
