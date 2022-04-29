from enum import Enum
from types import FunctionType
from .tool import FunctionContainer, add_func, get_container

_event_dict = {}


class Type(Enum):
    """
    The type of events: (PRE, PERIOD, POST).
    """
    PRE = 0
    PERIOD = 1
    POST = 2


class Priority(Enum):
    """
    The priority of function execution
    """
    HIGHEST = 0
    HIGHER = 1
    NORMAL = 2
    LOW = 3
    LOWER = 4
    LOWEST = 5

    @staticmethod
    def parse_priority(obj):
        if isinstance(obj, Priority):
            return obj
        if isinstance(obj, int):
            obj = max((obj, 0))
            obj = min((obj, 5))
            return Priority(obj)
        return Priority.NORMAL


class Event:
    """
    The parent class of every single event you create.
    """

    def __init__(self, event_type=Type.PRE):
        """
        :param event_type: The type of the event.
        """
        self.type = event_type
        self.cancelled = False

    def __eq__(self, other):
        return self.type == other.type and self.cancelled == other.cancelled and self.__class__ == other.__class__

    def call(self):
        """
        Trigger a event, and call all functions related to this specific event.
        """
        if self.__class__ not in _event_dict:
            return
        funcs = _event_dict.get(self.__class__)
        for func in funcs:
            func.exec_func(self)
            if self.cancelled:
                break


class EventHandler:
    """
    EventHandler makes a certain function subscribe to one to multiple event classes.
    This means whenever a event with the class is triggered, the function will be called.
    """

    def __init__(self, *events, priority=Priority.NORMAL):
        self.priority = Priority.parse_priority(priority)
        self.events = [x for x in events if issubclass(x, Event) or x == Event]

    def __call__(self, func):
        if not isinstance(self.priority, Priority):
            self.priority = Priority.NORMAL

        if not isinstance(func, FunctionType):
            return

        if func.__code__.co_argcount != 1:
            return

        for event in self.events:
            if event in _event_dict:
                add_func(func, self.priority, _event_dict[event])
            else:
                _event_dict[event] = [FunctionContainer(func, self.priority)]

        return func


def get_function_names(event):
    """
    :param event: The specific event class.
    :return: A list containing all the names of functions that subscribed to the given event.
    """
    if event not in _event_dict:
        return []
    return [f.func.__name__ for f in _event_dict[event]]


def get_functions(event):
    """
    :param event: The specific event class.
    :return: A list containing all the function objects that subscribed to the given event.
    """
    if event not in _event_dict:
        return []
    return [x.func for x in _event_dict[event]]


def get_function_containers(event):
    """
    :param event: The specific event class.
    :return: A list containing all the function containers that subscribed to the given event.
    """
    if event not in _event_dict:
        return []
    return [x.func for x in _event_dict[event]]


def set_priority(func, event, priority):
    """
    Set the priority of the given func in the given event.
    raises RuntimeError it func or event doesn't exist.
    """
    no_priority = FunctionContainer(func, -1)
    if event not in _event_dict or no_priority not in _event_dict[event]:
        raise RuntimeError("You can't set the priority if it doesn't exist.")
    get_container(_event_dict[event], func, no_priority).priority = Priority.parse_priority(priority)


def get_priority(func, event):
    """
    :return: priority of the function (return None if func or event doesn't exist)
    """
    if event not in _event_dict:
        return None
    no_priority = FunctionContainer(func, -1)
    if no_priority not in _event_dict[event]:
        return None
    return get_container(_event_dict[event], func, no_priority).priority


def unsubscribe(func, *events):
    """
    :param func: The function that unsubscribes the certain event.
    :param events: The event classes to unsubscribe from.
    Unsubscribe one to multiple events.
    """
    to_remove = FunctionContainer(func, -1)
    for event in events:
        if event not in _event_dict or to_remove not in _event_dict[event]:
            continue
        _event_dict[event].remove(to_remove)


def subscribe(func, *events, priority=Priority.NORMAL):
    """
    :param func: The function that subscribes the certain event.
    :param events: The event classes to subscribe to.
    :param priority: The priority of function execution
    subscribe an event.
    """
    EventHandler(events, priority=priority)(func)


def contains_func(func, event):
    """
    :param func: Any function.
    :param event: Any event class.
    :return whether func subscribed to event.
    """
    if event not in _event_dict:
        return False
    return FunctionContainer(func, -1) in _event_dict[event]


def clear_event(event):
    """
    :param event: the event class to unsubscribe from.
    Make all the functions that subscribed the given event unsubscribe it.
    """
    if event not in _event_dict:
        return
    _event_dict[event] = []


def install_event(event):
    """
    :param event: The event class that need to be used.
    Use the event in any module without importing anything.
    """
    if __name__ == "__main__":
        raise RuntimeError()
    if not issubclass(event, Event) and event != Event:
        return
    __import__("builtins").__dict__[event.__name__] = event
