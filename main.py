import telebot, dotenv, os
from dotenv import load_dotenv
from currency_converter import CurrencyConverter


load_dotenv()
TOKEN = os.getenv("TOKEN")
bot = telebot.telebot()
currency = CurrencyConverter()


@bot.message_handler(commands=['start'])


bot.polling(none_stop=True)