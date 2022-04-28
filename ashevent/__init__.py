"""
AshEvent
======
A simple event system in Python
"""

from .event import *

__name__ = "ashevent"
__version__ = "0.2"
__all__ = [
    "VERSION", "AUTHOR", "Type", "Event", "EventHandler",
    "get_function_names", "get_functions", "unsubscribe",
    "subscribe", "contains_func", "unsubscribe_all",
    "install_event", "install_only", "install_module", "install_all",
]
