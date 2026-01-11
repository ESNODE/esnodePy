class FunctionBoundary:
    def __init__(self, name, declared_return=None):
        self.name = name
        self.declared_return = declared_return
        self.observed_returns = set()

    def observe_return(self, value_type):
        self.observed_returns.add(value_type)

    def has_drift(self):
        if not self.declared_return:
            return False
        return self.declared_return not in self.observed_returns
