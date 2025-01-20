# main.py

import pyray as pr
from core.py_redux.action_creators import (
    set_position,
    reset_position,
    set_velocity,
    reset_velocity,
    set_input,
    reset_input,
)


def main():
    pr.init_window(800, 600, "Action Tester")
    pr.set_target_fps(60)

    position = {"x": 400, "y": 300}
    velocity = {"x": 0, "y": 0}
    input_state = {"up": False, "down": False, "left": False, "right": False}

    while not pr.window_should_close():
        # Input handling
        input_state["up"] = pr.is_key_down(pr.KEY_W)
        input_state["down"] = pr.is_key_down(pr.KEY_S)
        input_state["left"] = pr.is_key_down(pr.KEY_A)
        input_state["right"] = pr.is_key_down(pr.KEY_D)

        if pr.is_key_pressed(pr.KEY_R):
            position = {"x": 400, "y": 300}
            velocity = {"x": 0, "y": 0}
            input_state = {"up": False, "down": False, "left": False, "right": False}

        # Update velocity based on input state
        velocity["x"] = 0
        velocity["y"] = 0

        if input_state["up"]:
            velocity["y"] -= 1
        if input_state["down"]:
            velocity["y"] += 1
        if input_state["left"]:
            velocity["x"] -= 1
        if input_state["right"]:
            velocity["x"] += 1

        # Apply velocity to position
        position["x"] += velocity["x"]
        position["y"] += velocity["y"]

        # Generate actions
        position_action = set_position(position["x"], position["y"])
        velocity_action = set_velocity(velocity["x"], velocity["y"])
        input_action = set_input(input_state)

        # Draw
        pr.begin_drawing()
        pr.clear_background(pr.RAYWHITE)

        pr.draw_text("Use W/A/S/D to toggle input states", 10, 10, 20, pr.DARKGRAY)
        pr.draw_text("Use Arrow Keys to change velocity", 10, 40, 20, pr.DARKGRAY)
        pr.draw_text("Press R to reset", 10, 70, 20, pr.DARKGRAY)

        pr.draw_text(f"Position: {position}", 10, 120, 20, pr.MAROON)
        pr.draw_text(f"Velocity: {velocity}", 10, 150, 20, pr.MAROON)
        pr.draw_text(f"Input: {input_state}", 10, 180, 20, pr.MAROON)

        pr.draw_text(f"Position Action: {position_action}", 10, 220, 20, pr.BLUE)
        pr.draw_text(f"Velocity Action: {velocity_action}", 10, 250, 20, pr.BLUE)
        pr.draw_text(f"Input Action: {input_action}", 10, 280, 20, pr.BLUE)

        pr.draw_circle(int(position["x"]), int(position["y"]), 10, pr.RED)

        pr.end_drawing()

    pr.close_window()


if __name__ == "__main__":
    main()
