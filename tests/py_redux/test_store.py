import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

# Import the action creators and action type constants.
from core.py_redux.action_creators import (
    set_position,
    reset_position,
    set_velocity,
    reset_velocity,
    set_input,
    reset_input,
)
from core.py_redux.actions import (
    SET_POSITION,
    SET_VELOCITY,
    SET_INPUT,
    RESET_POSITION,
    RESET_VELOCITY,
    RESET_INPUT,
)

# Import your store creator and root reducer.
# It’s assumed you have implemented these in your project.
from core.py_redux.store import create_store, root_reducer


class TestReducers(unittest.TestCase):
    def setUp(self):
        # Define the default initial state.
        self.initial_state = {
            "position": {"x": 400, "y": 300},
            "velocity": {"x": 0, "y": 0},
            "input": {"up": False, "down": False, "left": False, "right": False},
        }

    def test_set_position(self):
        action = set_position(100, 150)
        # Pass the action through the reducer.
        new_state = root_reducer(self.initial_state, action)
        self.assertEqual(new_state["position"], {"x": 100, "y": 150})

    def test_reset_position(self):
        # Create a modified state that is different from default.
        modified_state = {
            **self.initial_state,
            "position": {"x": 100, "y": 150},
        }
        action = reset_position()
        new_state = root_reducer(modified_state, action)
        self.assertEqual(new_state["position"], self.initial_state["position"])

    def test_set_velocity(self):
        action = set_velocity(5, -3)
        new_state = root_reducer(self.initial_state, action)
        self.assertEqual(new_state["velocity"], {"x": 5, "y": -3})

    def test_reset_velocity(self):
        modified_state = {
            **self.initial_state,
            "velocity": {"x": 5, "y": -3},
        }
        action = reset_velocity()
        new_state = root_reducer(modified_state, action)
        self.assertEqual(new_state["velocity"], self.initial_state["velocity"])

    def test_set_input(self):
        new_input = {"up": True, "down": False, "left": True, "right": False}
        action = set_input(new_input)
        new_state = root_reducer(self.initial_state, action)
        self.assertEqual(new_state["input"], new_input)

    def test_reset_input(self):
        modified_state = {
            **self.initial_state,
            "input": {"up": True, "down": True, "left": True, "right": True},
        }
        action = reset_input()
        new_state = root_reducer(modified_state, action)
        self.assertEqual(new_state["input"], self.initial_state["input"])


class TestStore(unittest.TestCase):
    def setUp(self):
        self.initial_state = {
            "position": {"x": 400, "y": 300},
            "velocity": {"x": 0, "y": 0},
            "input": {"up": False, "down": False, "left": False, "right": False},
        }
        self.store = create_store(root_reducer, self.initial_state)

    def test_initial_state(self):
        # Ensure the store’s initial state is correct.
        self.assertEqual(self.store.get_state(), self.initial_state)

    def test_dispatch_set_position(self):
        # Dispatch an action to update the position.
        self.store.dispatch(set_position(200, 250))
        state = self.store.get_state()
        self.assertEqual(state["position"], {"x": 200, "y": 250})

    def test_dispatch_sequence(self):
        # Dispatch a sequence of actions.
        self.store.dispatch(set_position(100, 100))
        self.store.dispatch(set_velocity(2, 3))
        new_input = {"up": True, "down": False, "left": False, "right": True}
        self.store.dispatch(set_input(new_input))

        state = self.store.get_state()
        self.assertEqual(state["position"], {"x": 100, "y": 100})
        self.assertEqual(state["velocity"], {"x": 2, "y": 3})
        self.assertEqual(state["input"], new_input)

        # Now dispatch resets.
        self.store.dispatch(reset_position())
        self.store.dispatch(reset_velocity())
        self.store.dispatch(reset_input())
        state = self.store.get_state()
        self.assertEqual(state, self.initial_state)


if __name__ == "__main__":
    unittest.main()
