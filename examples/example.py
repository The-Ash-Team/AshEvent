# import ashevent, you can also use install_all() *not recommended*.
from ashevent import *


# define our own event, inherits Event class.
class MessageReceiveEvent(Event):
    def __init__(self, msg):
        super().__init__(EventType.POST)  # do the super init (POST because you can't get msg before or while sending).
        self.msg = msg  # custom property msg.


# subscribed to the event we just defined,
# and also the Event class (yes this is possible I don't know if I should remove this)
@EventHandler(MessageReceiveEvent, Event)
def onEvents(e):  # the priority is NORMAL by default.
    if e.__class__ != MessageReceiveEvent:  # we subscribed to 2 events, so we should check this..
        print("A Event just happened")
        return
    msg = e.msg
    if msg == "priority":
        print("[Normal]: NORMAL!")  # won't be working. (check onMessageEvent to know why!)
    elif msg == "cool":
        print("cool")
    elif msg == "clearEvent":  # this will clear Event (all functions subscribed to Event will unsubscribe from it)
        clear_event(Event)  # this is how you use it: simple!
        print("cleared!")
    elif msg == "tell me all functions subscribed to MessageReceiveEvent pls":
        print(get_function_names(MessageReceiveEvent))


# this function has the HIGHEST priority, so when a MessageReceiveEvent is called, it will be executed first!
@EventHandler(MessageReceiveEvent, priority=Priority.HIGHEST)
def onMessageReceive(e):
    msg = e.msg
    if msg == "priority":
        print("[HIGHEST]: I'm the coolest!!!")
        e.msg = "cool"  # makes what onEvents function get is 'cool'
    elif msg == "time":  # shows the time!
        import time
        print("The time now: " + time.strftime("%X"))
    elif msg.lower() == "event":
        Event().call()  # triggers a new Event, and onEvents function will get it !! owo!!
    # sub & unsub (shows you how to use subscribe() unsubscribe() and contains_func())
    elif msg == "unsub":
        # contains_func tells you whether a func subscribed to a type of event
        if not contains_func(onEvents, MessageReceiveEvent):
            print("OnEvents doesn't subscribe to MessageReceiveEvent")
            return
        unsubscribe(onEvents, MessageReceiveEvent)  # unsubscribe (you can pass in multiple event types)!
        print("onEvents no longer subscribes to MessageReceiveEvent")
    elif msg == "sub":
        if contains_func(onEvents, MessageReceiveEvent):
            print("OnEvents already subscribed to MessageReceiveEvent")
            return
        subscribe(onEvents, MessageReceiveEvent)
        print("onEvents now subscribes to MessageReceiveEvent")
    # sets the priority (shows you how to use set_priority() and get the priority of a FunctionContainer)
    elif msg == "low":
        if onMessageReceive.priority == Priority.LOW:  # this method's priority is already LOW
            print("Yo, im already low priority, please make me the highest by typing in highest")
            return
        set_priority(onMessageReceive, MessageReceiveEvent, Priority.LOW)  # sets the priority to low
        #  and sort the list (so the functions be executed in the correct order)
        print("My priority is LOW now!!! NOOOOOO!!!")
    elif msg == "highest":
        if onMessageReceive.priority == 0:  # ye you can compare Priority with an int
            print("Man, i'm already on the top")
            return
        set_priority(onMessageReceive, MessageReceiveEvent, Priority.HIGHEST)
        print("gg let's goooo! Back again with da highest priority!!!!!")


# create the main loop
if __name__ == "__main__":
    while (message := input("Enter your message: ")) != "exit" and message != "quit":
        event = MessageReceiveEvent(message)  # yeah! instantiate our class!
        event.call()  # yeah! use the call() method!
