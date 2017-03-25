trigger spec
============

There are two types of triggers: active triggers and passive triggers. Passive triggers are called on a regular interval specified by the trigger (for example every 5 minutes) to check if the trigger is satisfied. Active triggers receive some sort of signal (for example an HTTP request) when they are satisfied. Most triggers will probably be passive.

### Passive triggers
Passive triggers should be coded using asyncio for scalability. The basic structure for a passive trigger is some asynchronous function which performs a synchronous task then defers another run of itself for a certain time later (5 seconds maybe). Each passive trigger should be decorated with the `passive` decorator. Below is an example.

```
@passive("Test", "This is a test trigger", args=[("Arg1", Int), ("Arg2", Int)], results=[("Choice", Int)])
async def test_trigger(arg1, arg2): 
    await asyncio.sleep(1)
    choice = random.random()

    return (choice < 0.1, choice)
```

### Active triggers
idk something