ashevent = None if __name__ == "__main__" else __import__("sys").modules["ashevent"]


class FunctionContainer:
    """
    Contain a function and a priority
    """
    def __init__(self, func, priority):
        self.func = func
        self.priority = priority

    def get_priority_value(self):
        """
        :return: The value of priority (LOWEST=5, HIGHEST=0)
        """
        return self.priority.value

    def exec_func(self, event):
        """
        execute the func using the given event as parameter
        """
        self.func(event)

    def __eq__(self, other):
        if not isinstance(other, FunctionContainer):
            return False
        return self.func is other.func and (self.priority == other.priority or other.priority == -1)


def sort_priority(funcs: list[FunctionContainer]):
    list.sort(funcs, key=FunctionContainer.get_priority_value)


def get_container(funcs, func, no_priority=None):
    if no_priority is None:
        no_priority = FunctionContainer(func, -1)
    if no_priority not in funcs:
        return None
    return funcs[funcs.index(no_priority)]


def add_func(func, priority, funcs: list[FunctionContainer]):
    container = FunctionContainer(func, priority)
    no_priority = FunctionContainer(func, -1)
    if container in funcs:
        return
    if no_priority in funcs:
        get_container(funcs, func, no_priority).priority = priority
    else:
        funcs.append(container)

    sort_priority(funcs)


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

