# action_creators.py
from .actions import (
    SET_POSITION,
    SET_VELOCITY,
    SET_INPUT,
    RESET_POSITION,
    RESET_VELOCITY,
    RESET_INPUT,
)

# Action Creators


# Position
def set_position(x, y):
    """Create an action to set the position."""
    return {"type": SET_POSITION, "payload": {"x": x, "y": y}}


def reset_position():
    """Create an action to reset the position to default."""
    return {"type": RESET_POSITION}


# Velocity
def set_velocity(x, y):
    """Create an action to set the velocity."""
    return {"type": SET_VELOCITY, "payload": {"x": x, "y": y}}


def reset_velocity():
    """Create an action to reset the velocity to default."""
    return {"type": RESET_VELOCITY}


# Input
def set_input(input_state):
    """Create an action to set the input state."""
    return {
        "type": SET_INPUT,
        "payload": input_state,  # Example: {"up": True, "down": False}
    }


def reset_input():
    """Create an action to reset the input state to default."""
    return {"type": RESET_INPUT}
