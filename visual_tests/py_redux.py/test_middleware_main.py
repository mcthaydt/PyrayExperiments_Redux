import logging
import pyray as pr
from core.py_redux.middleware import MiddlewareManager, LoggerMiddleware
from core.py_redux.store import create_store, root_reducer
from core.py_redux.action_creators import set_position, set_velocity, set_input
from core.py_redux.reducers import DEFAULT_POSITION, DEFAULT_VELOCITY, DEFAULT_INPUT

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Initialize Pyray
pr.init_window(800, 600, "Pyray Middleware Example")
pr.set_target_fps(60)

# Initial state
initial_state = {
    "position": DEFAULT_POSITION,
    "velocity": DEFAULT_VELOCITY,
    "input": DEFAULT_INPUT,
}

# Create store and middleware
store = create_store(root_reducer, initial_state)
middleware_manager = MiddlewareManager(store, [LoggerMiddleware()])

# Main game loop
while not pr.window_should_close():
    # Handle input
    input_state = {
        "up": pr.is_key_down(pr.KEY_W),
        "down": pr.is_key_down(pr.KEY_S),
        "left": pr.is_key_down(pr.KEY_A),
        "right": pr.is_key_down(pr.KEY_D),
    }
    middleware_manager.dispatch(set_input(input_state))

    # Update velocity based on input
    input = store.get_state()["input"]
    velocity = {
        "x": -5 if input["left"] else 5 if input["right"] else 0,
        "y": -5 if input["up"] else 5 if input["down"] else 0,
    }
    middleware_manager.dispatch(set_velocity(velocity["x"], velocity["y"]))

    # Update position based on velocity
    state = store.get_state()
    position = state["position"]
    velocity = state["velocity"]
    new_position = {
        "x": position["x"] + velocity["x"],
        "y": position["y"] + velocity["y"],
    }
    middleware_manager.dispatch(set_position(new_position["x"], new_position["y"]))

    # Rendering
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)

    # Draw rectangle at updated position
    pr.draw_rectangle(new_position["x"], new_position["y"], 50, 50, pr.BLUE)

    pr.end_drawing()

# Close window
pr.close_window()
