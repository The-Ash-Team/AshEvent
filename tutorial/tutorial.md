# AshEvent

## Introduction
&emsp;AshEvent helps you create and control events easily.  
&emsp;This is all the things you will have to do to implement a simple event system:  
 - Create an event in order to describe a thing that happens.
 - Create one or multiple functions that subscribe to that event and handles it.
 - When it's the right time, call the event, and all the functions will be executed!

## Installation
&emsp;You use `pip install ashevent` to install AshEvent. If you also want to specify the version, like 0.3.1, just do `pip install ashevent==0.3.1`. When a new version comes out, and you want to update, do `pip install --upgrade ashevent`.

## Usage

### Importing
&emsp;First, like all the other modules, you `import ashevent`. You can give it a shorter name by `import ashevent as ae`. If you are lazy and don't want to type too much, just do `from ashevent import *`.  
&emsp;This is basically everything you need to know about importing! But if you want to learn more complicated skills, please keep reading.  
&emsp;AshEvent also provides functions that enable you to use certain properties in every module without importing. These functions start with `install_`. The thing after `install_` is what you can use in all modules without importing. You should be very careful when using these functions. Here's a list of things that you should remember.

1. Using these functions will be confusing, so try not to use them!
2. The better way of doing this is `from a import b` and `import a`. Just use `import` if you can.
3. You can't use any properties before installing them, so write your code in the correct order.
4. You shouldn't install things with names of built-in functions or classes.
5. When you use an installed property, your IDE may tell you it's wrong, but it's actually not.

### Creating Events
&emsp;After importing ashevent, we can finally create our events. It's actually very simple, You write a class that inherits the `Event` class. Here is an example (we created a MessageReceiveEvent):
```python
from ashevent import *

class MessageReceiveEvent(Event):
    def __init__(self, msg):
        super().__init__(EventType.POST)  # EventType.POST because the event happens after the user types a message.
        self.msg = msg  # store the value so that we can use it afterwards.
```
&emsp;Simple, right? But you still have something to think about here. You should choose the `EventType` wisely because it can be used in our event functions. If you would like to, you can call three events with different EventTypes before, during, and after an event, and our event functions will do different things depending on the EventType. The reason we make it POST here is that we can't get a message before or while the user is typing.

### Creating Event Functions 
&emsp;A simple event class isn't all we want. We also want some functions to handle that event. That is what event functions do! An event function is a function that subscribes to a type of event and handles it. This type of function takes an argument 'event'. The value of it is the event object that is being called. When a function subscribes to an event class, it's no longer a function, it's a `FunctionContainer` which contains the original function and the priority.   
&emsp;But how do we make a function subscribe to an event class? It's also very simple. Just use `@EventHandler`. And if you want to set the priority, use `Priority`. Here is an example:
```python
@EventHandler(MessageReceiveEvent, Event, priority=Priority.NORMAL)
def onEvents(e):  # the priority is NORMAL by default, so the 'priority=Priority.NORMAL' is unnecessary here.
    if type(e) != MessageReceiveEvent:  # we subscribed to 2 events, so we should check this.
        print("An Event just happened")
        return
    msg = e.msg
    if msg == "cool":
        print("cool")
```
&emsp;In that example, function `onEvents` subscribed to 2 events: `Event` and `MessageReceiveEvent`.(Yes, you can subscribe to the `Event` class, I don't know if it's a good idea to keep this feature) Now, if an `Event` is called, our program will output: "An Event just happened", if a MessageReceiveEvent with `msg='cool'` is called, our program will say: "cool".

### Instantiate and Calling Our Events
&emsp;Now, we've created an event class and a function to handle that kind of event. It's time to instantiate and call our event.  
&emsp;If you instantiated a class before, you should know how it works. You write the name of the class, and put A pair of brackets after that. Between the two brackets, put the necessary arguments, and the `__init__` method of that class will be called with the arguments you passed in. Just like this: `my_event = MessageReceiveEvent('cool')`, we've created a `MessageReceiveEvent` object.  
&emsp;Now, we use the method in `Event` class to call `my_event`. You do it like this `my_event.call()`. If you have finished all the coding, congratulations! You have implemented a simple event system with AshEvent. 


## The End
Thanks for reading this tutorial! I hope you have learned the basic usage of this module! If you want to learn more, check the [examples](https://github.com/The-Ash-Team/AshEvent/tree/main/examples).  
<br>
_Written by Za08_