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
currencies_list = currency.currencies
currencies_list.remove('RUB')


@bot.message_handler(commands=['start'])
def start(message):
    '''
    Function that allows bot to send a message with an amount request after /start command in bot
    '''
    bot.send_message(message.chat.id, 'Hello, enter amount to convert')
    bot.register_next_step_handler(message, amount)


def amount(message):
    '''
    Function that takes amount to convert, draws buttons and handles incorrect input values
    '''
    global amount
    try:
        amount = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, 'Incorrect amount: it should be numerical value. Try again.')
        bot.register_next_step_handler(message, amount)
        return

    if amount > 0:
        markup = types.InlineKeyboardMarkup(row_width=2)
        btn_usd_eur = types.InlineKeyboardButton('USD / EUR', callback_data='usd/eur')
        btn_eur_usd = types.InlineKeyboardButton('EUR / USD', callback_data='eur/usd')
        btn_jpy_eur = types.InlineKeyboardButton('JPY / EUR', callback_data='jpy/eur')
        btn_jpy_usd = types.InlineKeyboardButton('JPY / USD', callback_data='jpy/usd')
        btn_else = types.InlineKeyboardButton('Custom', callback_data='else')
        markup.add(btn_usd_eur, btn_eur_usd, btn_jpy_eur, btn_jpy_usd, btn_else)
        bot.send_message(message.chat.id, 'Choose currency pair', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Incorrect amount: it should be more than 0. Try again.')
        bot.register_next_step_handler(message, amount)


@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    '''
    Function that works with callback data from buttons, described in amount(message) function
    and actually converts entered amount
    '''
    if call.data != 'else':
        values = call.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(call.message.chat.id, f'Today, entered {amount} {values[0]} makes {res:.2f} {values[1]}')
        bot.send_message(call.message.chat.id, 'If you want to convert another value, enter it here')
        bot.register_next_step_handler(call.message, amount)
    else:
        bot.send_message(call.message.chat.id, f'Enter custom currencies in CUR/CUR format. Available currencies:\n{currencies_list}')
        bot.register_next_step_handler(call.message.chat.id, my_currency)


def my_currency(message):
    try:
        values = message.data.upper().split('/')
        res = currency.convert(amount, values[0], values[1])
        bot.send_message(message.chat.id, f'Today, entered {amount} {values[0]} makes {res:.2f} {values[1]}')
        bot.send_message(message.chat.id, 'If you want to convert another value, enter it here')
        bot.register_next_step_handler(message, amount)
    except Exception:
        bot.send_message(message.chat.id, f'Something went wrong. Enter amount again')
        bot.register_next_step_handler(message, my_currency)




bot.infinity_polling()