import pyray as pr
from core.py_redux.store import create_store, root_reducer
from core.py_redux.action_creators import (
    set_position,
    set_velocity,
    set_input,
    reset_position,
    reset_velocity,
    reset_input,
)

# Initialize Pyray and window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

pr.init_window(SCREEN_WIDTH, SCREEN_HEIGHT, "Redux + Pyray Visual Test")
pr.set_target_fps(FPS)

# Initialize the store
initial_state = {
    "position": {"x": 400, "y": 300},
    "velocity": {"x": 0, "y": 0},
    "input": {"up": False, "down": False, "left": False, "right": False},
}

store = create_store(root_reducer, initial_state)

# Game loop
while not pr.window_should_close():
    # Input handling
    input_state = {
        "up": pr.is_key_down(pr.KEY_W),
        "down": pr.is_key_down(pr.KEY_S),
        "left": pr.is_key_down(pr.KEY_A),
        "right": pr.is_key_down(pr.KEY_D),
    }
    store.dispatch(set_input(input_state))

    # Update velocity based on input
    current_input = store.get_state()["input"]
    velocity = {"x": 0, "y": 0}

    if current_input["up"]:
        velocity["y"] -= 5
    if current_input["down"]:
        velocity["y"] += 5
    if current_input["left"]:
        velocity["x"] -= 5
    if current_input["right"]:
        velocity["x"] += 5

    store.dispatch(set_velocity(velocity["x"], velocity["y"]))

    # Update position based on velocity
    current_position = store.get_state()["position"]
    current_velocity = store.get_state()["velocity"]

    new_position = {
        "x": current_position["x"] + current_velocity["x"],
        "y": current_position["y"] + current_velocity["y"],
    }

    # Keep the object within the window boundaries
    new_position["x"] = max(0, min(SCREEN_WIDTH, new_position["x"]))
    new_position["y"] = max(0, min(SCREEN_HEIGHT, new_position["y"]))

    store.dispatch(set_position(new_position["x"], new_position["y"]))

    # Handle reset with R key
    if pr.is_key_pressed(pr.KEY_R):
        store.dispatch(reset_position())
        store.dispatch(reset_velocity())
        store.dispatch(reset_input())

    # Render
    pr.begin_drawing()
    pr.clear_background(pr.RAYWHITE)

    # Display debug text
    state = store.get_state()
    debug_text = f"""
    Position: x={state['position']['x']}, y={state['position']['y']}
    Velocity: x={state['velocity']['x']}, y={state['velocity']['y']}
    Input: up={state['input']['up']}, down={state['input']['down']}, 
           left={state['input']['left']}, right={state['input']['right']}
    Press R to Reset
    """
    pr.draw_text("Use W/A/S/D to move", 10, 10, 20, pr.DARKGRAY)
    pr.draw_text(debug_text, 10, 40, 10, pr.DARKGRAY)

    # Draw the object at the current position
    position = state["position"]
    pr.draw_circle(int(position["x"]), int(position["y"]), 20, pr.BLUE)

    pr.end_drawing()

# Clean up
pr.close_window()
