# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

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
