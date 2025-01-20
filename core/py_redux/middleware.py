import logging


class Middleware:
    """Base middleware class."""

    def process(self, store, next_action, action):
        """Default process method to be overridden by subclasses."""
        next_action(action)


class LoggerMiddleware(Middleware):
    """Logger middleware that logs state changes."""

    def process(self, store, next_action, action):
        # Log the state before the action
        logging.info("State before action: %s", store.get_state())
        logging.info("Processing action: %s", action)

        # Call the next middleware or reducer
        next_action(action)

        # Log the state after the action
        logging.info("State after action: %s", store.get_state())


class MiddlewareManager:
    """Manages middleware processing for dispatched actions."""

    def __init__(self, store, middlewares):
        self.store = store
        self.middlewares = middlewares

    def dispatch(self, action):
        def apply_middleware(index):
            if index < len(self.middlewares):
                self.middlewares[index].process(
                    self.store, lambda a: apply_middleware(index + 1), action
                )
            else:
                self.store.dispatch(action)

        apply_middleware(0)
