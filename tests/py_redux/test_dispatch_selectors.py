import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import pytest
import unittest

# Import the classes and functions to be tested.
# Adjust the import paths if your project structure is different.
from core.py_redux.dispatch import DispatchManager
from core.py_redux.selectors import get_position, get_velocity, get_input


# Dummy middleware for testing purposes.
class DummyMiddleware:
    def __init__(self):
        self.processed_actions = []

    def process(self, action):
        self.processed_actions.append(action)


# Dummy store for testing purposes.
class DummyStore:
    def __init__(self):
        self.dispatched_actions = []

    def dispatch(self, action):
        self.dispatched_actions.append(action)


class TestDispatchManager(unittest.TestCase):
    def setUp(self):
        # Create dummy store and middleware instances.
        self.store = DummyStore()
        self.middleware1 = DummyMiddleware()
        self.middleware2 = DummyMiddleware()
        self.dispatch_manager = DispatchManager(
            store=self.store, middlewares=[self.middleware1, self.middleware2]
        )

        # Define a sample action to dispatch.
        self.action = {"type": "TEST_ACTION", "payload": 42}

    def test_dispatch_calls_middlewares_and_store(self):
        """Test that the DispatchManager calls all middleware.process
        and then calls store.dispatch with the action."""
        self.dispatch_manager.dispatch(self.action)

        # Verify that each middleware processed the action.
        self.assertEqual(
            self.middleware1.processed_actions,
            [self.action],
            "Middleware1 did not process the action as expected.",
        )
        self.assertEqual(
            self.middleware2.processed_actions,
            [self.action],
            "Middleware2 did not process the action as expected.",
        )

        # Verify that the store received the action.
        self.assertEqual(
            self.store.dispatched_actions,
            [self.action],
            "Store did not dispatch the action as expected.",
        )


class TestSelectors(unittest.TestCase):
    def setUp(self):
        # Create a sample state dictionary.
        self.state = {
            "position": (10, 20),
            "velocity": (1, 2),
            "input": "user_input_data",
        }

    def test_get_position(self):
        """Test the get_position selector."""
        expected = (10, 20)
        result = get_position(self.state)
        self.assertEqual(
            result, expected, f"Expected position {expected} but got {result}."
        )

    def test_get_velocity(self):
        """Test the get_velocity selector."""
        expected = (1, 2)
        result = get_velocity(self.state)
        self.assertEqual(
            result, expected, f"Expected velocity {expected} but got {result}."
        )

    def test_get_input(self):
        """Test the get_input selector."""
        expected = "user_input_data"
        result = get_input(self.state)
        self.assertEqual(
            result, expected, f"Expected input {expected} but got {result}."
        )


if __name__ == "__main__":
    unittest.main()
