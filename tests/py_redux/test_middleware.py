import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest
from unittest.mock import Mock
import logging

from core.py_redux.middleware import Middleware, LoggerMiddleware


class TestLoggerMiddleware(unittest.TestCase):
    def setUp(self):
        # Mock store with get_state and dispatch
        self.store = Mock()
        self.store.get_state = Mock(return_value={"counter": 0})
        self.store.dispatch = Mock()

        # Mock next function
        self.next = Mock()

        # Initialize LoggerMiddleware instance
        self.middleware = LoggerMiddleware()

    def test_logger_middleware_no_state_change(self):
        """LoggerMiddleware should log even if the state doesn't change."""
        action = {"type": "NO_OP"}

        with self.assertLogs(level=logging.INFO) as log:
            self.middleware.process(self.store, self.next, action)

        # Assert that logs contain state before and after
        self.assertIn("State before action:", log.output[0])
        self.assertIn("Processing action:", log.output[1])
        self.assertIn("State after action:", log.output[2])

        # Ensure the next action was called
        self.next.assert_called_once_with(action)

    def test_logger_middleware_empty_action(self):
        """LoggerMiddleware should handle an empty action gracefully."""
        action = {}

        with self.assertLogs(level=logging.INFO) as log:
            self.middleware.process(self.store, self.next, action)

        # Assert that logs contain state before and after
        self.assertIn("State before action:", log.output[0])
        self.assertIn("Processing action:", log.output[1])
        self.assertIn("State after action:", log.output[2])

        # Ensure the next action was called
        self.next.assert_called_once_with(action)

    def test_logger_middleware_null_action(self):
        """LoggerMiddleware should handle a None action gracefully."""
        action = None

        with self.assertLogs(level=logging.INFO) as log:
            self.middleware.process(self.store, self.next, action)

        # Assert that logs contain state before and after
        self.assertIn("State before action:", log.output[0])
        self.assertIn("Processing action:", log.output[1])
        self.assertIn("State after action:", log.output[2])

        # Ensure the next action was called
        self.next.assert_called_once_with(action)

    def test_logger_middleware_large_state(self):
        """LoggerMiddleware should handle large state objects."""
        # Simulate a large state
        self.store.get_state = Mock(return_value={"data": list(range(1000))})
        action = {"type": "UPDATE_DATA"}

        with self.assertLogs(level=logging.INFO) as log:
            self.middleware.process(self.store, self.next, action)

        # Assert that logs contain state before and after
        self.assertIn("State before action:", log.output[0])
        self.assertIn("Processing action:", log.output[1])
        self.assertIn("State after action:", log.output[2])

        # Ensure the next action was called
        self.next.assert_called_once_with(action)

    def test_logger_middleware_multiple_actions(self):
        """LoggerMiddleware should handle multiple actions dispatched sequentially."""
        actions = [{"type": "INCREMENT"}, {"type": "DECREMENT"}]

        for action in actions:
            with self.assertLogs(level=logging.INFO) as log:
                self.middleware.process(self.store, self.next, action)

            # Assert that logs contain state before and after for each action
            self.assertIn("State before action:", log.output[0])
            self.assertIn("Processing action:", log.output[1])
            self.assertIn("State after action:", log.output[2])

            # Ensure the next action was called for each
            self.next.assert_called_with(action)


if __name__ == "__main__":
    unittest.main()
