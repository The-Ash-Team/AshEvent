from enum import Enum
from types import FunctionType


ashevent = None if __name__ == "__main__" else __import__("sys").modules["ashevent"]
_event_dict = {}
VERSION = "0.2"
AUTHOR = "Za08"


class Type(Enum):
    """
    The type of events: (PRE, PERIOD, POST).
    """
    PRE = 0
    PERIOD = 1
    POST = 2


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
        for event_class in _event_dict:
            if event_class != self.__class__:
                return
            funcs = _event_dict.get(event_class)
            for func in funcs:
                func(self)


class EventHandler:
    """
    EventHandler makes a certain function subscribe to one to multiple event classes.
    This means whenever a event with the class is triggered, the function will be called.
    """

    def __init__(self, *event_classes):
        self.classes = [x for x in event_classes if issubclass(x, Event) or x == Event]

    def __call__(self, func):
        if not isinstance(func, FunctionType):
            return

        if func.__code__.co_argcount != 1:
            return

        for clazz in self.classes:
            if clazz in _event_dict:
                _event_dict[clazz].append(func)
            else:
                _event_dict[clazz] = [func]

        return func


def get_function_names(event):
    """
    :param event: The specific event class.
    :return: A list containing all the names of functions that subscribed to the given event.
    """
    if event not in _event_dict:
        return []
    return [f.__name__ for f in _event_dict[event]]


def get_functions(event):
    """
    :param event: The specific event class.
    :return: A list containing all the function objects that subscribed to the given event.
    """
    if event not in _event_dict:
        return []
    return _event_dict[event]


def unsubscribe(func, event):
    """
    :param func: The function that unsubscribes the certain event.
    :param event: The event class to unsubscribe from.
    Unsubscribe a event.
    """
    if event not in _event_dict:
        return
    _event_dict[event].remove(func)


def subscribe(func, event):
    """
    :param func: The function that subscribes the certain event.
    :param event: The event class to subscribe to.
    Unsubscribe an event.
    """
    if event in _event_dict and func in _event_dict[event]:
        return
    EventHandler(event)(func)


def contains_func(func, event):
    """
    :param func: Any function.
    :param event: Any event class.
    :return whether func subscribed to event.
    """
    if event not in _event_dict:
        return False
    return func in _event_dict[event]


def unsubscribe_all(event):
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


def install_only(name: str):
    """
    :param name: The name of a function, class, etc. in this module (ashevent).
    Use the property in any module without importing.
    """
    if __name__ == "__main__":
        raise RuntimeError()
    props = {x: eval("ashevent." + x) for x in ashevent.__all__}
    if name in props:
        __import__("builtins").__dict__[name] = eval(name)


def install_module():
    """
    Use ashevent in any module without importing
    """
    if __name__ == "__main__":
        raise RuntimeError()
    __import__("builtins").__dict__[ashevent.__name__] = ashevent


def install_all():
    """
    Use all the properties in ashevent in any module without importing
    """
    if __name__ == "__main__":
        raise RuntimeError()
    props = {x: eval("ashevent." + x) for x in ashevent.__all__}
    __import__("builtins").__dict__.update(**props)
