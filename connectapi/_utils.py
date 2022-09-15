from typing import Dict

__version__ = "0.1.1a0"


def remove_none_from_dict(d: Dict):
    return {k: v for k, v in d.items() if v is not None}
