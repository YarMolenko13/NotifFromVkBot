# Taskkill /PID python.exe /F
# импорты из библиотек
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
# from aiogram.api.methods.send_media_group import SendMediaGroup

import asyncio

# импорты из других py файлов
from config import *
from parserVK import WallParse
from db import Postgers
from keyboards import write_kb


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

parser = WallParse()

db = Postgers()


# commands хэндлеры
@dp.message_handler(commands=['start'])
async def process_start_cmd(message: types.Message):
	text = 'Давай начнем\nВот мои команды: \n- /subscribe\n- /unsubscribe'
	db.set_state(message.from_user.id, 1)
	await message.reply(text, reply=True)


@dp.message_handler(commands=['subscribe'])
async def subscribe(message: types.Message):
	text = 'Введите ссылку или домен группы в вк,\nчтобы я отправлял вам новые посты 😁\nМаксимум 7 групп.'
	db.set_state(message.from_user.id, 2)
	await bot.send_message(message.from_user.id, text)


@dp.message_handler(commands=['unsubscribe'])
async def unsubscribe(message: types.Message):
	text = 'Выбирете сообщество, от которого \nвы не хотите получать посты 👇'
	db.set_state(message.from_user.id, 3)
	await message.reply(text, reply_markup=write_kb(message.from_user.id))



# state хэндлеры
@dp.message_handler(lambda message: db.get_current_state(message.from_user.id) == 2)
async def write_notif(message: types.Message):

	domain = message.text.split('/')[-1].strip()
	# обрабатываем выброс моей страницы
	if parser.test(domain):
		text = 'Ссылка или домен недействительны (:'
		await bot.send_message(message.from_user.id, text)
	else:
		if db.get_count_sub_pub(message.from_user.id) <= 7:
			await bot.send_message(message.from_user.id, 'Достигунт максимум сообществ (')
		else:
			db.subscribe(message.from_user.id, domain)
			data = parser.get_data(domain)
			id_post = data['id_post']
			date_post = data['date']

			db.set_state(message.from_user.id, 1)

			db.insert_post_data(domain,id_post, date_post)

			await bot.send_message(message.from_user.id, 'Excellent! Рассылка подключена. \nВот последний пост в этой группы: ', disable_notification=False)

			# name_pub = parser.get_pub_name(domain)
			# text = 'В паблике "' + name_pub + '" новый пост:'
			# await bot.send_message(message.from_user.id, text)

			text = data['text']
			if text != '':
				await bot.send_message(message.from_user.id, text)

			imgs = data['img_list']
			if len(imgs) > 1:
				media = types.MediaGroup()
				for img in imgs:
					media.attach_photo(img)
				await bot.send_media_group(message.from_user.id, media=media, disable_notification=True)
			else:
				if len(imgs) == 1:
					await bot.send_photo(message.from_user.id, photo=imgs[0], disable_notification=True)
				else:
					pass

			videos = data['video_list']
			if len(videos) != 0:
				for video in videos:
					await bot.send_message(message.from_user.id, video)


@dp.message_handler(lambda message: db.get_current_state(message.from_user.id) == 3)
async def unsubscribe_pub(message: types.Message):
	domain = message.text.split('/')[-1].strip()
	name = message.text.split('/')[0].strip()
	db.unsubscribe(message.from_user.id, domain)
	text = 'Хорошо, рассылка от ' + name + ' отключена'
	await bot.send_message(message.from_user.id, text)


# таймер
async def scheduled(wait_for):
	while True:
		await asyncio.sleep(wait_for)

		rows = db.get_all_rows()
		for row in rows:
			await asyncio.sleep(2)

			id = row[0]
			user_id = row[1]
			domain = row[2]
			id_post_db = row[3]

			try:
				id_post_parsed = parser.get_data(domain)['id_post']
			except:
				await asyncio.sleep(0.5)
				id_post_parsed = parser.get_data(domain)['id_post']

			if id_post_db != id_post_parsed:

				db.set_new_post(user_id, id_post_parsed, domain)

				try:
					name_pub = parser.get_pub_name(domain)
				except:
					await asyncio.sleep(0.7)
					name_pub = parser.get_pub_name(domain)

				text = 'В паблике "' + name_pub + '" новый пост:'
				await bot.send_message(user_id, text)

				text = parser.get_data(domain)['text']
				if text != '':
					await bot.send_message(user_id, text)

				imgs = parser.get_data(domain)['img_list']
				if len(imgs) > 1:
					media = types.MediaGroup()
					for img in imgs:
						media.attach_photo(img)
					await bot.send_media_group(user_id, media=media, disable_notification=True)
				else:
					if len(imgs) == 1:
						await bot.send_photo(user_id, photo=imgs[0], disable_notification=True)
					else:
						pass

				videos = parser.get_data(domain)['video_list']
				if len(videos) != 0:
					for video in videos:
						await bot.send_message(user_id, video)
		


if __name__ == '__main__':
	dp.loop.create_task(scheduled(360))
	executor.start_polling(dp)









