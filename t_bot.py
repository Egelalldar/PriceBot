import telebot

#from telebot import types
from mysql import add_user, add_url
from secrets import secrets

bot = telebot.TeleBot(secrets["token"])

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	# # Создание клавиатуры
	# keyboard = types.ReplyKeyboardMarkup(row_width=2)
	# button1 = types.KeyboardButton('Кнопка 1')
	# button2 = types.KeyboardButton('Кнопка 2')
	# button3 = types.KeyboardButton('Кнопка 3')
	# keyboard.add(button1, button2, button3)
	# bot.reply_to(message, "keyboard?", reply_markup=keyboard)
	bot.reply_to(message, "HI?")
	if add_user(str(message.from_user.id)):
		bot.send_message(message.chat.id, "user added")
	else:
		bot.send_message(message.chat.id,"user already added")

@bot.message_handler(commands=['add'])
def send_url_part_1(message):
	bot_message = bot.reply_to(message, 'paste url')
	bot.register_next_step_handler(bot_message, send_url_part_2)
def send_url_part_2(message):
	url = message.text
	if add_url(message.chat.id, url):
		bot.reply_to(message, 'url added')
	else:
		bot.reply_to(message, '''/start
		or url exist''')



@bot.message_handler(func=lambda message: True)
def simple_message(message):
	bot.reply_to(message, '/start, /help, /add')

bot.polling()