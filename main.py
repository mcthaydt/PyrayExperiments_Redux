import logging
import math
import pyray
from core.py_redux.store import create_store, root_reducer
from core.py_redux.action_creators import set_position, set_velocity, set_input
from core.py_redux.selectors import get_position, get_velocity, get_input
from core.py_redux.middleware import LoggerMiddleware, MiddlewareManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initial game state
initial_state = {
    "position": {"x": 400, "y": 300},
    "velocity": {"x": 0, "y": 0},
    "input": {"up": False, "down": False, "left": False, "right": False},
}

# Create the store and middleware manager
store = create_store(root_reducer, initial_state)
logger_middleware = LoggerMiddleware()
middleware_manager = MiddlewareManager(store, [logger_middleware])


def handle_input():
    """Update the input state based on keyboard input."""
    input_state = {
        "up": pyray.is_key_down(pyray.KEY_W),
        "down": pyray.is_key_down(pyray.KEY_S),
        "left": pyray.is_key_down(pyray.KEY_A),
        "right": pyray.is_key_down(pyray.KEY_D),
    }
    middleware_manager.dispatch(set_input(input_state))


def update_velocity():
    """Update the velocity based on the current input state."""
    state = store.get_state()
    input_state = get_input(state)
    velocity = get_velocity(state)

    # Acceleration factor
    accel = 0.5
    max_speed = 5

    # Update velocity based on input
    new_velocity_x = velocity["x"] + (
        accel if input_state["right"] else -accel if input_state["left"] else 0
    )
    new_velocity_y = velocity["y"] + (
        accel if input_state["down"] else -accel if input_state["up"] else 0
    )

    # Clamp velocity to max speed
    new_velocity_x = max(-max_speed, min(max_speed, new_velocity_x))
    new_velocity_y = max(-max_speed, min(max_speed, new_velocity_y))

    # Dispatch the updated velocity
    middleware_manager.dispatch(set_velocity(new_velocity_x, new_velocity_y))


def update_position():
    """Update the position based on the current velocity and handle bouncing."""
    state = store.get_state()
    position = get_position(state)
    velocity = get_velocity(state)

    # Update position
    new_position_x = position["x"] + velocity["x"]
    new_position_y = position["y"] + velocity["y"]

    # Screen boundaries
    screen_width = 800
    screen_height = 600
    radius = 20

    # Check for collisions with walls and reverse velocity if needed
    if new_position_x - radius < 0 or new_position_x + radius > screen_width:
        velocity["x"] = -velocity["x"]  # Reverse x-velocity
        new_position_x = max(radius, min(screen_width - radius, new_position_x))

    if new_position_y - radius < 0 or new_position_y + radius > screen_height:
        velocity["y"] = -velocity["y"]  # Reverse y-velocity
        new_position_y = max(radius, min(screen_height - radius, new_position_y))

    # Dispatch the updated position and velocity
    middleware_manager.dispatch(set_position(new_position_x, new_position_y))
    middleware_manager.dispatch(set_velocity(velocity["x"], velocity["y"]))


def draw_state():
    """Draw the state information on the screen."""
    state = store.get_state()
    position = get_position(state)
    velocity = get_velocity(state)
    input_state = get_input(state)

    # Draw state information
    pyray.draw_text(f"Position: {position}", 10, 10, 20, pyray.BLACK)
    pyray.draw_text(f"Velocity: {velocity}", 10, 40, 20, pyray.BLACK)
    pyray.draw_text(f"Input: {input_state}", 10, 70, 20, pyray.BLACK)

    # Draw velocity vector
    pyray.draw_line_ex(
        (int(position["x"]), int(position["y"])),
        (
            int(position["x"] + velocity["x"] * 50),
            int(position["y"] + velocity["y"] * 50),
        ),
        2,
        pyray.BLUE,
    )

    # Draw the circle representing the position
    pyray.draw_circle(int(position["x"]), int(position["y"]), 20, pyray.MAROON)


def main():
    """Main game loop."""
    pyray.init_window(800, 600, "Pyray + Redux Example")
    pyray.set_target_fps(60)

    while not pyray.window_should_close():
        # Update game state
        handle_input()
        update_velocity()
        update_position()

        # Draw the current state
        pyray.begin_drawing()
        pyray.clear_background(pyray.RAYWHITE)

        draw_state()

        pyray.end_drawing()

    pyray.close_window()


if __name__ == "__main__":
    main()
