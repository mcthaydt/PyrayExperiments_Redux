# selectors.py
def get_position(state):
    """Retrieve the position from the state."""
    return state["position"]


def get_velocity(state):
    """Retrieve the velocity from the state."""
    return state["velocity"]


def get_input(state):
    """Retrieve the input state."""
    return state["input"]
