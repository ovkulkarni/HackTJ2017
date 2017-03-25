from triggers.RSSTrigger import RSSTrigger

import asyncio

async def start():
    trig = RSSTrigger()
    await trig.init("http://lorem-rss.herokuapp.com/feed?unit=second&interval=30")

    await trig.call()

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()
