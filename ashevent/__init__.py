"""
AshEvent
======
A simple event system in Python
"""

from .event import *
from .tool import (install_all, install_only, install_module)

__author__ = "Za08"
__version__ = "0.3.1"
__all__ = [
    "EventType", "Event", "EventHandler", "Priority",
    "get_function_names", "get_functions", "get_function_containers",
    "unsubscribe", "subscribe", "contains_func", "clear_event", "set_priority",
    "install_event", "install_only", "install_module", "install_all",
]
