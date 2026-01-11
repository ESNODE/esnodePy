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
    def __init__(self, name: str, declared_return: Optional[str] = None, file: Optional[str] = None, lineno: Optional[int] = None):
        """
        Initialize a FunctionBoundary.

        Args:
            name (str): The name of the function.
            declared_return (Optional[str]): The return type declared in the signature.
            file (Optional[str]): The file path where the function is defined.
            lineno (Optional[int]): The line number where the function is defined.
        """
        self.name: str = name
        self.declared_return: Optional[str] = declared_return
        self.file: Optional[str] = file
        self.lineno: Optional[int] = lineno
        self.observed_returns: Set[str] = set()

    def observe_return(self, value: str) -> None:
        """
        Record an observed return value shape.

        Args:
            value (str): The string representation of the observed return shape.
        """
        self.observed_returns.add(value)

    def has_drift(self) -> bool:
        """
        Check if the observed behavior contradicts the declared assumption.
        
        Drift definition (v0.2):
        - A return type is declared (and is not 'None').
        - But we observe a 'None' return (implicit or explicit).

        Returns:
            bool: True if drift is detected, False otherwise.
        """
        if not self.declared_return:
            return False

        # If declared is explicitly None, observing None is fine.
        if self.declared_return == "None":
            return False

        # If declared is NOT None, but we observe None (or implicit None), that's a risk.
        # Check for our specific None markers.
        for obs in self.observed_returns:
            if obs == "None" or obs == "None (implicit)":
                return True

        return False
