# Copyright (c) 2024 ESTIMATEDSTOCKS AB & KHAJAMODDIN SHAIK. All Rights Reserved.
#
# This software is released under the ESNODE COMMUNITY LICENSE 1.0.
# See the LICENSE file in the root directory for full terms and conditions.

from typing import Dict, Any


def run(target_dir: str = ".") -> Dict[str, Any]:
    """Runtime observation is local-only for security reasons.

    The current implementation is a placeholder and returns a message
    describing the feature status.
    """
    return {"message": "Runtime observation is opt-in and not enabled by default.", "local_path": target_dir}
