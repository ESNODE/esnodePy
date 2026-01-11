# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

from typing import Optional, Set

class FunctionBoundary:
    """
    Represents a function boundary where assumptions (declarations) 
    vs reality (observations) can be compared.
    """
    def __init__(self, name: str, declared_return: Optional[str] = None):
        """
        Initialize a FunctionBoundary.

        Args:
            name (str): The name of the function.
            declared_return (Optional[str]): The return type declared in the signature.
        """
        self.name: str = name
        self.declared_return: Optional[str] = declared_return
        self.observed_returns: Set[str] = set()

    def observe_return(self, value_type: str) -> None:
        """
        Record an observed return type from runtime or static analysis.

        Args:
            value_type (str): The string representation of the observed type.
        """
        self.observed_returns.add(value_type)

    def has_drift(self) -> bool:
        """
        Check if the observed behavior contradicts the declared assumption.

        Returns:
            bool: True if drift is detected, False otherwise.
        """
        # If no declaration exists, we cannot determine drift (strictness is off)
        if not self.declared_return:
            return False
        
        # In a more complex engine, we would check for subclass compatibility.
        # For v0.1, we check for strict string equality or membership.
        return self.declared_return not in self.observed_returns
