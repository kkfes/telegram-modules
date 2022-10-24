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
			us = None
			try:
				us = infList[args_list[0]]
			except:
				us = None
			addtxt = ''
			if us!=None:
				addtxt='<s>'+us[0]+'</s> -'
			infList[user] = [str(count), time]
			self.db.set("KMod", "infList", infList)
			await utils.answer(
				message,
				f"✅ Пользователь <code>{args_list[0]}</code> добавлен в список заражений!\n"
				f"ℹ️ Число: {addtxt}<code>{count}</code>\n"
				f"📅 Дата: <b>{time}</b>"
			)
		else:
			if not reply: 
				return await utils.answer(message, '❎ Реплай должен быть на смс ириса "<b>...подверг заражению...</b>"')
			elif not 'подверг заражению' in reply.text and not 'подвергла заражению' in reply.text:
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
				us = None
				try:
					us = infList[user]
				except:
					us = None
				addtxt = ''
				if us!=None:
					addtxt='<s>'+us[0]+'</s> -'
				infList[user] = [t, time]
				self.db.set("KMod", "infList", infList)
				await utils.answer(message, f"✅ Пользователь <code>{user}</code> добавлен в список заражений.\nℹ️ Число: {addtxt}<code>{count}</code>\n📅 Дата: <b>{time}</b>")


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
			await utils.answer(message, f"<b>✅ Жертва <code>{args_list[0]}</code>:\n☣️ {user[0]} био-опыта.\n📆 Дата: <i>{user[1]}</i></b>")
		except:
			await utils.answer(message, "❎ Данного пользователя нет в списке.")

	async def zarrmcmd(self, message):
		"Удаляет ид из списка"
		infList = self.db.get("KMod", "infList")
		args = utils.get_args_raw(message)
		args_list = args.split(' ')
		try:
			infList.pop(args_list[0])
			self.db.set("KMod", "infList", infList)
			await utils.answer(message, f"🗑 Пользователь <code>{args}</code> удалён из списка.")
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
					idx2 = messag[i].rindex("|")
					give = messag[i][idx1+1:idx2-6]
					t = str(give)
					t = t.replace(",", "." )
					while "|" in t:
						t=t[t.index("|")+1:(len(t)-1)]
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

	async def zarupdatecmd(self, message):
		"Ответом на мои жертвы (обновит информацию о жертве)"
		infList = self.db.get("KMod", "infList")
		reply = await message.get_reply_message()
		txt = '<b>🖋 Вот все добавленные жертвы:</b>\n'
		timezone = "Europe/Kiev"
		time = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
		messag = reply.message.split('\n')
		i = 1
		for value in reply.entities:
			if 'tg://openmessage?user_id=' in value.url:
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
						idx2 = messag[i].rindex("|")
						give = messag[i][idx1+1:idx2]
						t = str(give)
						t = t.replace(",", "." )
						t = t.replace("+", "" )
						t = t.strip()
						while "|" in t:
							t=t[t.index("|")+1:(len(t)-1)]
						num1 = 0
						if 'k' in t:
							tn = float(t[0:(len(t)-1)])
							tn=tn*1000
							t=str(tn)
						num1 = float(t)
						user, count = str(text), float(num1)
						us = None
						try:
							us = infList[text]
						except:
							us = None
						addtxt = ''
						if us!=None:
							addtxt='<s>'+us[0]+'</s> -'
						infList[user] = [str(count), time]
						self.db.set("KMod", "infList", infList)
						txt+=str(i)+'. '+text+' - '+addtxt+'<code>'+str(num1)+'</code>\n'
				except Exception as e:
					txt+=str(i)+' '+str(e)+'\n'
			i=i+1

		return await utils.answer(message,txt)

	async def zarfiltercmd(self, message):
		"""  {args1} {args2 OR reply} \nВызови команду, чтобы просмотреть аргументы."""
		args = utils.get_args_raw(message)
		reply = await message.get_reply_message()
		filter_and_users = self.db.get("KMod", "numfilter", {'users': [], 'filter': None, 'status': False})
		if not args:
			return await utils.answer(message, f"➕ <code>add</code> --- добавить|удалить юзеров(не больше 10), на которых будет триггериться фильтр(ид|реплай).\n[{', '.join(list('<code>' + i + '</code>' for i in filter_and_users['users']))}]\n❔ <code>pref</code> --- установить фильтр. Допустим один.\n<code>{filter_and_users['filter'] if filter_and_users['filter'] else '❌Не установлен.'}</code>\n<code>start</code> --- запустить|остановить.\n<b>{'✅ Статус: Запущен' if filter_and_users['status'] else '❌ Статус: Остановлен'}.</b>\n\n📝 Работает так:\n[фильтр] чек @id - проверка жертвы\n[фильтр] чеклист/[фильтр] зарчек/[фильтр] листчек - проверка списка биотоп/биотоп чата/биотоп корп\n[фильтр] доб @id ресы (без К) - добавит пользователя в зарлист")
		args = args.split(' ', maxsplit=1)
		if len(args) == 1 and not reply and args[0] != 'start':
			return await utils.answer(message, '❌ Нет 2 аргумента и реплая.')
		elif args[0] == 'add':
			try:
				user_id = args[1]
				if not user_id.isdigit():
					return await utils.answer(message, 'Это не ид.')
			except:
				user_id = str(reply.sender_id)
			if user_id in filter_and_users['users']:
				filter_and_users['users'].remove(user_id)
				await utils.answer(message, f"✅ Ид <code>{user_id}</code> удалён.")
			elif len(filter_and_users['users']) <= 10:
				filter_and_users['users'].append(user_id)
				await utils.answer(message, f"✅ Ид <code>{user_id}</code> добавлен.")
			else:
				return await utils.answer(message, '❌ Превышен лимит в 10 юзеров.')
			return self.db.set("KMod", "numfilter", filter_and_users)
		elif args[0] == 'pref':
			try:
				filter_and_users['filter'] = args[1].lower().strip()
				self.db.set("KMod", "numfilter", filter_and_users)
				return await utils.answer(message, f"✅ Фильтр ~~~ <code>{args[1]}</code> ~~~ успешно установлен!")
			except:
				return await utils.answer(message, "Где 2 аргумент❓")
		elif args[0] == 'start':
			if filter_and_users['status']:
				filter_and_users['status'] = False
				self.db.set("KMod", "numfilter", filter_and_users)
				return await utils.answer(message, "❌ Фильтр остановлен.")
			else:
				filter_and_users['status'] = True
				self.db.set("KMod", "numfilter", filter_and_users)
				return await utils.answer(message, "✅ Фильтр запущен.")
		else:
			return await utils.answer(message, "❌ Неизвестный аргумент.")


	async def watcher(self, message):
		if not isinstance(message, telethon.tl.types.Message): return
		filter_and_users = self.db.get("KMod", "numfilter", {'users': [], 'filter': None, 'status': False})
		user_id = str(message.sender_id)
		if not filter_and_users['filter'] or not filter_and_users['status'] or user_id not in filter_and_users['users'] or message.is_private: return
		text = message.raw_text.lower()
		if not text.startswith(filter_and_users['filter']): return
		text=text.replace(filter_and_users['filter'],'')
		text=text.strip()
		key = ''
		try:
			key = text[0:text.index(' ')]
		except:
			key = text[0:len(text)]
		key=key.strip()
		text=text.replace(key,'')
		text=text.strip()
		if key=='чек':
			if "@" in text:
				infList = self.db.get("KMod", "infList")
				try:
					idd = text[text.index("@"):len(text)]
					user = infList[text[text.index("@"):len(text)]]
					await message.respond(f"<b>✅ Жертва <code>{idd}</code>:\n☣️ {user[0]} био-опыта.\n📆 Дата: <i>{user[1]}</i></b>")
				except:
					await message.respond("❎ Данного пользователя нет в списке.")
			else:
				await message.respond("❎ Укажите ид вместе с @")
		elif key=='листчек' or key=='зарчек' or key=='чеклист':
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
						idx2 = messag[i].rindex("|")
						give = messag[i][idx1+1:idx2-6]
						t = str(give)
						t = t.replace(",", "." )
						while "|" in t:
							t=t[t.index("|")+1:(len(t)-1)]
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
			return await message.respond(txt)
		elif key=='доб':
			infList = self.db.get("KMod", "infList")
			timezone = "Europe/Kiev"
			time = datetime.now(pytz.timezone(timezone)).strftime("%d.%m")
			reply = await message.get_reply_message()
			args_list = text.split(' ')
			if len(args_list)==2:
				try:
					user, count = str(args_list[0]), float(args_list[1])
				except:
					await message.respond( "❎ Данные были введены не корректно")
					return

				infList[user] = [str(count), time]
				self.db.set("KMod", "infList", infList)
				await message.respond(
					f"✅ Пользователь <code>{args_list[0]}</code> добавлен в список заражений!\n"
					f"ℹ️ Число: <code>{count}</code>\n"
					f"📅 Дата: <b>{time}</b>"
				)
			else:
				if not reply: 
					return await message.respond( '❎ Реплай должен быть на смс ириса "<b>...подверг заражению...</b>"')
				elif not 'подверг заражению' in reply.text and not 'подвергла заражению' in reply.text:
					return await message.respond( '❎ Реплай должен быть на смс ириса "<b>...подверг заражению...</b>"')
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
					await message.respond( f"✅ Пользователь <code>{user}</code> добавлен в список заражений.\nℹ️ Число: <code>{count}</code>\n📅 Дата: <b>{time}</b>")
