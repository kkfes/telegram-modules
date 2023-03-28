# meta developer: @kkfes

from .. import loader, utils
from os import getpid
import asyncio, pytz, re, telethon
import traceback
import string, pickle

class PidMod(loader.Module):
    "Iris Biowar module"
    strings = {"name": "PidMod"}
    async def pidcmd(self, message):
        "Get pid"
        await utils.answer(message,'PID of my precess: '+str(getpid()))
