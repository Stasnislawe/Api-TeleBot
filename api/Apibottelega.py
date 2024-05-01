import telebot
import os
from config import keys
from extensions import APIException, Converter
from digitize import Exact
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv('TOKEN'))

@bot.message_handler(commands=['start','help'])
def help(message: telebot.types.Message):
    text = 'Вы можете посмотреть список валют - /values\nЧтобы начать работу введите команду боту в следующем формате:\n<имя валюты> <в какую валюту перевести> <количество>\nПример:"евро доллар 50"'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def converter(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Неправильное значение параметров.')

        base = values[0].lower()
        quote = values[1].lower()
        amount = values[2]
        priceonlyodnogo = Converter.get_price(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользвателя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не могу обработать команду\n{e}')
    else:
        var = Exact
        total_base = (var.discharge(float(priceonlyodnogo) * float(amount)))
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()
