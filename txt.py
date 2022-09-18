# meta developer: @kkfes

from .. import loader, utils
import logging
import asyncio


logger = logging.getLogger(__name__)


@loader.tds
class TxtMod(loader.Module):
    """Managing a second account is easy and simple"""

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
        if message.is_reply:
            use_reply = True
        txtq = (await message.get_reply_message()) if use_reply else message
        txtq.message = " ".join(args[0:])

        await utils.answer(message, txtq.message)
