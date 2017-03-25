import asyncio


class PassiveTrigger:
    _results = asyncio.Queue()

    def __init__(self):
        self.loop = asyncio.get_event_loop()

    def add_result(self, condition, **kwargs):
        self._results.put_nowait((condition, kwargs))

class Result:
    pass

class StringResult(Result):
    def __init__(self, name):
        self.name = name

class Arg:
    pass

class StringArg(Arg):
    def __init__(self, name):
        self.name = name

