from triggers.RSSTrigger import RSSTrigger
from events.Twilio import SendSMSEvent 

import asyncio

triggers = []

async def start():
    trig = RSSTrigger()
    await trig.init("http://lorem-rss.herokuapp.com/feed?unit=second&interval=30")
    triggers.append(trig)

    await trig.call()

async def monitor():
    for trig in triggers:
        while not trig._results.empty():
            res = trig._results.get_nowait()
            if not res[0]:
                continue

            ev = SendSMSEvent() 
            
            loop.create_task(ev.call("+15713582032", "New post: {}: {}".format(res[1]['title'], res[1]['text'])))

    await asyncio.sleep(5)
    loop.create_task(monitor())

def main():
    global loop
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.create_task(monitor())
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()
