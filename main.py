import telebot, dotenv, os
from dotenv import load_dotenv
from currency_converter import CurrencyConverter
from telebot import types


# first initializations of variables, objects etc
load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN)
currency = CurrencyConverter()
amount = 0


@bot.message_handler(commands=['start'])
def start(message):
    '''
    Function that allows bot to send a message with an amount request after /start command in bot
    '''
    bot.send_message(message.chat.id, 'Hello, enter amount to convert')
    bot.register_next_step_handler(message, amount)


def amount(message):
    global amount
    amount = message.text.strip()



bot.polling(none_stop=True)