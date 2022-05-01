from enum import Enum
from typing import (Dict, Any, List, Callable, Type, Union)

from .tool import FunctionContainer, add_func, sort_containers

_event_dict: Dict[Any, List[FunctionContainer]] = {}


class EventType(Enum):
    """
    Event Type, describes the happening time of an event  (PRE, PERIOD, POST).
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

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Priority):
            return self is other
        elif isinstance(other, int):
            return self.value == other
        return False

    @staticmethod
    def parse_priority(obj: Any) -> Enum:
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

    def __init__(self, event_type: EventType = EventType.PRE):
        """
        :param event_type: Type of the event.
        """
        self.type = event_type
        self.cancelled = False

    def __eq__(self, other: Any) -> bool:
        return self.type == other.type and self.cancelled == other.cancelled and self.__class__ == other.__class__

    def call(self):
        """
        Triggers a event, and calls all functions related to this specific event.
        """
        if self.__class__ not in _event_dict:
            return
        funcs = _event_dict.get(self.__class__)
        for func in funcs.copy():
            func.exec_func(self)
            if self.cancelled:
                break


class EventHandler:
    """
    EventHandler makes a certain function subscribe to one to multiple event classes.
    This means whenever an event with the class is triggered, the function will be called.
    """

    def __init__(self, *events, priority: Priority = Priority.NORMAL):
        self.priority = Priority.parse_priority(priority)
        self.events = [x for x in events if issubclass(x, Event) or x == Event]

    def __call__(self, func: Callable[[Event], None]) -> Union[Callable, FunctionContainer]:
        if not isinstance(self.priority, Priority):
            self.priority = Priority.NORMAL

        if not isinstance(func, Callable):
            return func

        if func.__code__.co_argcount != 1:
            return func

        container = FunctionContainer(func, self.priority)
        for event in self.events:
            if event in _event_dict:
                add_func(container, _event_dict[event])
            else:
                _event_dict[event] = [container]

        return container


def get_function_names(event: Type[Event]) -> List[str]:
    """
    :param event: The specific event class.
    :return: A list containing all the names of functions that subscribed to the given event.
    """
    if event not in _event_dict:
        return []
    return [f.func.__name__ for f in _event_dict[event]]


def get_functions(event: Type[Event]) -> List[Callable[[Event], None]]:
    """
    :param event: The specific event class.
    :return: A list containing all the function objects that subscribed to the given event.
    """
    if event not in _event_dict:
        return []
    return [x.func for x in _event_dict[event]]


def get_function_containers(event: Type[Event]) -> List[FunctionContainer]:
    """
    :param event: The specific event class.
    :return: A list containing all the function containers that subscribed to the given event.
    """
    if event not in _event_dict:
        return []
    return _event_dict[event].copy()


def unsubscribe(func: FunctionContainer, *events):
    """
    :param func: The function that unsubscribes the certain event.
    :param events: The event classes to unsubscribe from.
    Unsubscribe one to multiple events.
    """
    for event in events:
        if event not in _event_dict or func not in _event_dict[event]:
            continue
        _event_dict[event].remove(func)


def subscribe(func: Union[FunctionContainer, Callable[[Event], None]], *events, priority: Priority = Priority.NORMAL):
    """
    :param func: The function that subscribes the certain event.
    :param events: The event classes to subscribe to.
    :param priority: The priority of function execution
    subscribe an event.
    """
    func = func if isinstance(func, Callable) else func.func
    EventHandler(*events, priority=priority)(func)


def contains_func(func: Union[FunctionContainer, Callable[[Event], None]], event: Type[Event]):
    """
    :param func: Any function.
    :param event: Any event class.
    :return whether func subscribed to event.
    """
    func = func if isinstance(func, FunctionContainer) else FunctionContainer(func, -1)
    if event not in _event_dict:
        return False
    return func in _event_dict[event]


def set_priority(func: FunctionContainer, event: Type[Event], priority: Union[Priority, int],
                 sort: bool = True) -> bool:
    """
    :return: succeeded or not
    """
    if event not in _event_dict or func not in _event_dict[event]:
        return False
    priority = Priority.parse_priority(priority)
    func.priority = priority
    if sort:
        sort_containers(_event_dict[event])


def sort_priority(event: Type[Event]):
    if event not in _event_dict:
        return
    sort_containers(_event_dict[event])


def clear_event(event: Type[Event]):
    """
    :param event: the event class to unsubscribe from.
    Makes all the functions that subscribed the given event unsubscribe it.
    """
    if event not in _event_dict:
        return
    _event_dict[event].clear()


def install_event(event: Type[Event]):
    """
    :param event: The event class that need to be used.
    Uses the event in any module without importing anything.
    """
    if __name__ == "__main__":
        raise RuntimeError()
    if not issubclass(event, Event) and event != Event:
        return
    __import__("builtins").__dict__[event.__name__] = event
