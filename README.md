# AshEvent 0.3

## Introduction
AshEvent implemented a very simple ``event system`` in Python.  
It works like this:  

You use ``@EventHandler`` to let the function below subscribe to a type of event.  
Suppose you defined a EventA class that inherits the ``Event`` class we provide.  
Also, EventA has a custom variable **msg**.  
You can write something like this:

```python
@EventHandler(EventA)
def onAHappened(event):
    print(event.msg)
```
Now whenever you instantiate EventA and use the call method: ```EventA('some string...').call()```,  
AshEvent will notice it and call the function ``onAHappened`` we just defined.  

This is how AshEvent basically works.  
Furthermore, You can use ``Priority`` to set the order for the functions to run.  
You can use ``unsubscribe`` function to make a function no longer subscribe to a type of event.  
And you can use ``type``, ``cancelled`` in an event to create different effects.  
Know more about AshEvent in [examples](https://github.com/The-Ash-Team/AshEvent/tree/main/examples)...
