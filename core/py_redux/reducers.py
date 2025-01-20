# reducers.py

from core.py_redux.actions import (
    SET_POSITION,
    RESET_POSITION,
    SET_VELOCITY,
    RESET_VELOCITY,
    SET_INPUT,
    RESET_INPUT,
)

# Define default states.
DEFAULT_POSITION = {"x": 400, "y": 300}
DEFAULT_VELOCITY = {"x": 0, "y": 0}
DEFAULT_INPUT = {"up": False, "down": False, "left": False, "right": False}


def position_reducer(state, action):
    if action["type"] == SET_POSITION:
        return {"x": action["payload"]["x"], "y": action["payload"]["y"]}
    elif action["type"] == RESET_POSITION:
        return DEFAULT_POSITION.copy()
    return state


def velocity_reducer(state, action):
    """
    Update the 'velocity' portion of the state based on the action.
    """
    if action["type"] == SET_VELOCITY:
        return {"x": action["payload"]["x"], "y": action["payload"]["y"]}
    elif action["type"] == RESET_VELOCITY:
        return DEFAULT_VELOCITY.copy()
    return state


def input_reducer(state, action):
    """
    Update the 'input' portion of the state based on the action.
    """
    if action["type"] == SET_INPUT:
        return action["payload"]
    elif action["type"] == RESET_INPUT:
        return DEFAULT_INPUT.copy()
    return state


def root_reducer(state, action):
    """
    Combine the reducers for position, velocity, and input.
    This function returns a new state dict by updating each branch.
    """
    return {
        "position": position_reducer(state.get("position"), action),
        "velocity": velocity_reducer(state.get("velocity"), action),
        "input": input_reducer(state.get("input"), action),
    }
