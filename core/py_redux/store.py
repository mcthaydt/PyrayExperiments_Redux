# store.py


class Store:
    def __init__(self, reducer, initial_state):
        self.reducer = reducer
        self.state = initial_state

    def dispatch(self, action):
        # Apply the reducer to update the state
        self.state = self.reducer(self.state, action)

    def get_state(self):
        return self.state


def create_store(reducer, initial_state):
    return Store(reducer, initial_state)


# Import and export root_reducer so that it can be imported from store.py.
from .reducers import root_reducer
