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
    '''
    
    '''
    global amount
    amount = message.text.strip()

    markup = types.InlineKeyboardMarkup(row_width=3)
    btn_usd_eur = types.InlineKeyboardButton('USD -> EUR', callback_data='usd/eur')
    btn_eur_usd = types.InlineKeyboardButton('EUR -> USD', callback_data='eur/usd')
    btn_uah_eur = types.InlineKeyboardButton('UAH -> EUR', callback_data='uah/eur')
    btn_uah_usd = types.InlineKeyboardButton('UAH -> USD', callback_data='uah/usd')
    markup.add(btn_usd_eur, btn_eur_usd, btn_uah_eur, btn_uah_usd)
    bot.send_message(message.chat.id, 'Choose currency pair', reply_markup=markup)
    



bot.polling(none_stop=True)