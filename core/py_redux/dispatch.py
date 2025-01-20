# dispatch.py
class DispatchManager:
    def __init__(self, store, middlewares=[]):
        self.store = store
        self.middlewares = middlewares

    def dispatch(self, action):
        """Pass the action through middleware chain before updating the store."""
        for middleware in self.middlewares:
            middleware.process(action)
        self.store.dispatch(action)
