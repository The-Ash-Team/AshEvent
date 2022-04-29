# import ashevent, you can also use install_all() *not recommended*.
from ashevent import *


# define our own event, inherits Event class.
class MessageReceiveEvent(Event):
    def __init__(self, msg):
        super().__init__(Type.POST)  # do the super init (POST because you can't get msg before or while sending).
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


# create the main loop
if __name__ == "__main__":
    while (message := input("Enter your message: ")) != "exit" != "quit":
        event = MessageReceiveEvent(message)  # yeah! instantiate our class!
        event.call()  # yeah! use the call() method!
