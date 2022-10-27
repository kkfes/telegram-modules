# meta developer: @kkfes

from .. import loader, utils
import logging
import asyncio


logger = logging.getLogger(__name__)


@loader.tds
class TxtMod(loader.Module):
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
        if message.is_reply:
            use_reply = True
        txtq = (await message.get_reply_message()) if use_reply else message
        txtq.message = " ".join(args[0:])

        await utils.answer(message, txtq.message)

    async def btncmd(self, message):
        """.btn number of button (from 0)"""
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

        if use_reply:
        	reply = await message.get_reply_message()
        	result = await reply.click(int(txtq.message))
        	text = result.message;
        	if text!=None:
        		await utils.answer(message,text)
        
    async def pingcmd(self, message):
        """Test your userbot ping"""
        start = time.perf_counter_ns()
        message = await utils.answer(message, "<code>🐻 Nofin...</code>")

        await utils.answer(
            message,
            "<emoji document_id=6321050180095313397>⏱</emoji> <b>Скорость отклика"
            " Telegram:</b> <code>"+round((time.perf_counter_ns() - start) / 10**6, 3)+"</code> <b>ms</b>\n<emoji"
            " document_id=5377371691078916778>😎</emoji> <b>Прошло с последней"
            " перезагрузки: "+utils.formatted_uptime()+"</b>")
        )
