# meta developer: @kkfes

from .. import loader, utils
import logging
import asyncio


logger = logging.getLogger(__name__)


@loader.tds
class SpamMod(loader.Module):
    """Annoys people really effectively"""

    strings = {
        "name": "Txt",
        "need_txt": "<b>U wot? I need something to send?</b>",
        "txt_urself": "<b>Go send urself.</b>"
    }

    async def txtcmd(self, message):
        """.txt <message>"""
        use_reply = False
        args = utils.get_args(message)
        logger.debug(args)
        if len(args) == 0:
            await utils.answer(message, self.strings("need_txt", message))
            return
        if len(args) == 1:
            if message.is_reply:
                use_reply = True
            else:
                await utils.answer(message, self.strings("nice_number", message))
                return
        count = 0
        spam = (await message.get_reply_message()) if use_reply else message
        spam.message = " ".join(args[0:])
        try:
            count = int(count)
        except ValueError:
            await utils.answer(message, self.strings(".", message))
            return
        if count < 1:
            await utils.answer(message, self.strings(".", message))
            return
        await message.delete()
        if count > 20:
            # Be kind to other people
            sleepy = 2
        else:
            sleepy = 0
        i = 0
        size = 1 if sleepy else 100
        while i < count:
            await asyncio.gather(
                *[message.respond(spam) for x in range(min(count, size))]
            )
            await asyncio.sleep(sleepy)
            i += size
        await self.allmodules.log(
            "spam", group=message.to_id, data=spam.message + " (" + str(count) + ")"
        )
