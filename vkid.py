# meta developer: @kkfes

from .. import loader, utils
import logging
import asyncio
from datetime import datetime, date, time
import asyncio, pytz, re, telethon


logger = logging.getLogger(__name__)


@loader.tds
class VkidMod(loader.Module):
    """Модуль для бота СНЮСОЕД"""

    strings = {
        "name": "Vkid",
    }

    async def client_ready(self):
        self._me = await self._client.get_me()

    async def watcher(self, message):
        fr = str(message.from_id)
        if fr == "5431891078":
            text = message.message
            if 'начало отпускать, пора вкинуться' in text:
                en = message.entities
                for value in en:
                    try:
                        if str(value.user_id) == str(self._me.id):
                            await message.respond("/vkid")
                            return await self._client.send_read_acknowledge(
                                message.peer_id,
                                message,
                                clear_mentions=True,
                            )
                    except Exception as e:
                        pass
            else 'вкинулся! Кайфанул на' in text:
                return await self._client.send_read_acknowledge(
                                message.peer_id,
                                message,
                                clear_mentions=True,
                            )
