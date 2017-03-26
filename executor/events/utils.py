import asyncio


class Event:
    def __init__(self):
        self.loop = asyncio.get_event_loop()

class Arg:
    pass

class StringArg(Arg):
    def __init__(self, name):
        self.name = name

