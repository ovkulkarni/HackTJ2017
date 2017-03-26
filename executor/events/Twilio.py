from .utils import Event, StringArg

import asyncio
import functools
from twilio.rest import TwilioRestClient

TWILIO_ACCOUNT_SID = "AC6af79af13657485080b4402290c4655a"
TWILIO_AUTH_TOKEN = "b2f31d4728b2c6d932de5decea27dc2d"

def get_client():
    return TwilioRestClient(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

class SendSMSEvent(Event):
    _name = "SendSMS"
    _description = "Send SMS"
    _args = [StringArg("number"), StringArg("message")]

    async def call(self, number, message):
        client = get_client()

        try:
            m = await self.loop.run_in_executor(None, functools.partial(client.messages.create, to=number, from_="+18563912886", body=message))
            return (True, )
        except TwilioRestException as e:
            return (False, str(e))
