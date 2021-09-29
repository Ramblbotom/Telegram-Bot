import telebot


from config import *
from extensions import Converter, APIException

exchanges = {
    'доллар': 'USD',
    'евро': 'EUR',
    'рубль': 'RUB'
}
TOKEN = "1928930034:AAFa17Nj7wSb_42cWVLtITl7uqzFdtg9fvQ"

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = "Я вас категорически приветствую!!!"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = "Для того, что бы узнать курс для необходимой валюты, введите запрос следующим образом - наименование искомой валюты, наименование валюты из которой переводится, сумма перевода"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, sym, amount = message.text.split()
    except ValueError:
        bot.reply_to(message, "Неверное количество параметров")

    try:
        new_price = Converter.get_price(base, sym, amount)
        bot.reply_to(message, f"Цена {amount} {base} в {sym} : {new_price}")
    except APIException as e:
        bot.reply_to(message, f"Ошибка в команде:\n{e}")

bot.polling()