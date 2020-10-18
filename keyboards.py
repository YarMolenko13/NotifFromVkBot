from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

from parserVK import WallParse
from db import Postgers


parser = WallParse()
db = Postgers()


def write_kb(user_id):
	domains = db.get_domains(user_id)

	domains_kb = ReplyKeyboardMarkup(resize_keyboard=False, one_time_keyboard=True)

	for domain in domains:
		pub_name = parser.get_pub_name(domain[0])

		pub_name_btn = KeyboardButton(pub_name + ' / '+ str(domain[0]))
		domains_kb.add(pub_name_btn)

	return domains_kb

# write_kb(1365882584)