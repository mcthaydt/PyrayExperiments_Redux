import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

import unittest

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


class TestActionCreators(unittest.TestCase):
    def test_set_position(self):
        action = set_position(10, 20)
        expected_action = {
            "type": SET_POSITION,
            "payload": {"x": 10, "y": 20},
        }
        self.assertEqual(action, expected_action)

    def test_reset_position(self):
        action = reset_position()
        expected_action = {"type": RESET_POSITION}
        self.assertEqual(action, expected_action)

    def test_set_velocity(self):
        action = set_velocity(5, -5)
        expected_action = {
            "type": SET_VELOCITY,
            "payload": {"x": 5, "y": -5},
        }
        self.assertEqual(action, expected_action)

    def test_reset_velocity(self):
        action = reset_velocity()
        expected_action = {"type": RESET_VELOCITY}
        self.assertEqual(action, expected_action)

    def test_set_input(self):
        input_state = {"up": True, "down": False, "left": False, "right": True}
        action = set_input(input_state)
        expected_action = {
            "type": SET_INPUT,
            "payload": input_state,
        }
        self.assertEqual(action, expected_action)

    def test_reset_input(self):
        action = reset_input()
        expected_action = {"type": RESET_INPUT}
        self.assertEqual(action, expected_action)


if __name__ == "__main__":
    unittest.main()
