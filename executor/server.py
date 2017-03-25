from triggers.RSSTrigger import RSSTrigger

import asyncio

async def start():
    trig = RSSTrigger()
    await trig.init("http://rss.nytimes.com/services/xml/rss/nyt/HomePage.xml")

    await trig.call()

def main():
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()
