from executor.triggers.RSSTrigger import RSSTrigger
from executor.triggers.utils import parse_trigger_args, parse_trigger_results
from executor.events.Twilio import SendSMSEvent 
from executor.events.utils import parse_event_args
from db import db
from programs.models import *

import asyncio
import json

event_map = {'sms': SendSMSEvent}
trigger_map = {'rss': RSSTrigger}

async def start():
    triggers = parse_triggers()
    for trig in triggers:
        await trig.init(*trig.args)

    await monitor(triggers)

async def call_event(ev, context):
    res = await ev.call(context)

    if not res[0]:
        print("Event failed: {}".format(res[1]))

    if ev.next_ is not None:
        loop.create_task(call_event(ev.next_, context))

async def call_trigger(tr):
    await tr.call({})

    while not tr._results.empty():
        res = tr._results.get_nowait()
        if not res[0]:
            continue
        context = {}
        context['id_{}'.format(tr.block_id)] = res[1]

        if tr.next_ is not None:
            loop.create_task(call_event(tr.next_, context))

async def monitor(triggers):
    for trig in triggers:
        loop.create_task(call_trigger(trig))

    await asyncio.sleep(5)
    loop.create_task(monitor(triggers))

def get_event(ev):
    return event_map[ev]()

def get_trigger(tr):
    return trigger_map[tr]()

def parse_block(bl):
    if bl.block_type == 't':
        tr = get_trigger(bl.trigger.trigger_type)
        parsed_args = parse_trigger_args(bl.trigger.args)
        parsed_results = parse_trigger_results(bl.trigger.results)
        tr.args = parsed_args
        tr.results = parsed_results
        tr.block_id = bl.id
        retb = tr

    elif bl.block_type == 'e':
        ev = get_event(bl.event.action)
        parsed_args = parse_event_args(bl.event.args)
        ev.args = parsed_args
        ev.block_id = bl.id
        retb = ev

    source_links = bl.source_link
    if len(source_links) > 0:
        next_block = parse_block(source_links[0].destination)
        retb.next_ = next_block

    return retb


def parse_triggers():
    triggers = []
    triggers_b = Block.select().where(Block.block_type == 't')
    for t in triggers_b:
        tr = parse_block(t)
        triggers.append(tr) 

    return triggers


def main():
    global loop
    db.connect()
    loop = asyncio.get_event_loop()
    loop.create_task(start())
    loop.run_forever()
    loop.close()

if __name__ == '__main__':
    main()
