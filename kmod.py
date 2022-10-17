# meta developer: @kkfes

from .. import loader, utils
import asyncio, pytz, re, telethon
from telethon.tl.types import MessageEntityTextUrl
import json as JSON
from datetime import datetime, date, time

class KMod(loader.Module):
	"Модуль проверки и сохраниния жертв Iris Bot"
	strings={"name": "KMod"}
	
	async def client_ready(self, client, db):
		self.db = db
		if not self.db.get("KMod", "infList", False):
			self.db.set("KMod", "infList", {})
	

	async def zaraddcmd(self, message):
		" ответом на сообщение ириса с заражением, добавит в список заражений (@is/name значение) БЕЗ К, писать 8700 т т.д"
		infList = self.db.get("KMod", "infList")
		timezone = "Europe/Kiev"
		time = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
		reply = await message.get_reply_message()
		args = utils.get_args_raw(message)
		args_list = args.split(' ')
		if len(args_list)==2:
			try:
				user, count = str(args_list[0]), float(args_list[1])
			except:
				await utils.answer(message, "❎ Данные были введены не корректно")
				return

			infList[user] = [str(count), time]
			self.db.set("NumMod", "infList", infList)
			await utils.answer(
				message,
				f"✅ Пользователь <code>{args_list[0]}</code> добавлен в список заражений!\n"
				f"ℹ️ Число: <code>{count}</code>\n"
				f"📅 Дата: <b>{time}</b>"
			)
		else:
			if not reply: 
				return await utils.answer(message, '❎ Реплай должен быть на смс ириса "<b>...подверг заражению...</b>"')
			elif reply.sender_id != 707693258 and not 'подверг заражению' in reply.text:
				return await utils.answer(message, '❎ Реплай должен быть на смс ириса "<b>...подверг заражению...</b>"')
			else: #☣
				text = reply.text
				x = text.index('☣')+4
				count = text[x:].split(' ', maxsplit=1)[0]
				t = str(count)
				t = t.replace(",", "." )
				if t.endswith('k'):
					tn = float(t[0:(len(t)-1)])
					tn=tn*1000
					t=str(tn)
				x = text.index('user?id=') + 8
				user = '@' + text[x:].split('"', maxsplit=1)[0]
				infList[user] = [t, time]
				self.db.set("KMod", "infList", infList)
				await utils.answer(message, f"✅ Пользователь <code>{user}</code> добавлен в список заражений.\nℹ️ Число: <code>{count}</code>\n📅 Дата: <b>{time}</b>")


	async def zarlistcmd(self, message):
		"Список всех заражений"
		infList = self.db.get("KMod", "infList")
		sms = '🌀 Список заражений:\n'
		for key, value in infList.items():
			sms+=f'<b>• <code>{key}</code> -- <code>{value[0]}</code> [<i>{value[1]}</i>]</b>\n'
		await utils.answer(message, sms)

	async def zarfcmd(self, message):
		"поиск заражений .zarf @id/@name"
		infList = self.db.get("KMod", "infList")
		args = utils.get_args_raw(message)
		args_list = args.split(' ')
		try:
			user = infList[args_list[0]]
			await utils.answer(message, f"<b>✅ Жертва <code>{args_list[0]}</code>:\n☣️{user[0]} био-опыта.\n📆 Дата: <i>{user[1]}</i></b>")
		except:
			await utils.answer(message, "❎ Данного пользователя нет в списке.")

	async def zarrmcmd(self, message):
		"Удаляет ид из списка"
		infList = self.db.get("KMod", "infList")
		args = utils.get_args_raw(message)
		args_list = args.split(' ')
		try:
			infList.pop(args_list[0])
			self.db.set("NumMod", "infList", infList)
			await utils.answer(message, f"Пользователь <code>{args}</code> удалён из списка.")
		except:
			await utils.answer(message, "❎ Данного пользователя нет в списке.")


	async def zarcheckcmd(self, message):
		"Ответом на биотоп/биотоп чата/биотоп корп"
		infList = self.db.get("KMod", "infList")
		reply = await message.get_reply_message()
		txt = '<b>👮 Вот все провереные жертвы:</b>\n'
		messag = reply.message.split('\n')
		i = 1
		for value in reply.entities:	
			try:
				text = '@'+value.url.split("=")[1]
				user = None
				try:
					user = infList[text]
				except:
					user = None
				if user!=None:
					num = float(user[0])
					idx1 = messag[i].index("|")
					idx2 = messag[i].index("|",idx1+1)
					give = messag[i][idx1+1:idx2-6]
					t = str(give)
					t = t.replace(",", "." )
					num1 = 0
					if t.endswith('k'):
						tn = float(t[0:(len(t)-1)])
						tn=tn*1000
						t=str(tn)
					num1 = float(t)/10
					if num1 > num:
						nnnn = num1-num
						if nnnn <= 20:
							txt+=str(i)+'. '+text+' - ➖ <code>'+str((num1-num))+'</code>\n'
						else:
							txt+=str(i)+'. '+text+' - ✅ <code>+'+str((num1-num))+'</code>\n'
					else:
						txt+=str(i)+'. '+text+' - ❌ <code>'+str((num1-num))+'</code>\n'
				else:
					txt+=str(i)+'. Нет информаций 😔\n'
			except Exception as e:
				txt+=str(i)+' '+str(e)+'\n'
			i=i+1
		return await utils.answer(message,txt)
