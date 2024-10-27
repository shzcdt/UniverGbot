# # my_list = ["Привет", "как", "дела?"]
# result = ""
# for item in my_list:
#     result += item + " "
# print(result)
#
# fruits = ['яблоко', 'груша', 'банан', 'яблоко', 'груша', 'яблоко']
# unique_fruits = []
# for fruit in fruits:
#     if fruit not in unique_fruits:
#         unique_fruits.append(fruit)
# print(unique_fruits)
#
# fruits = ['яблоко', 'груша', 'банан', 'яблоко', 'груша', 'яблоко']
# unique_fruits = list(set(fruits))
# print(unique_fruits)
#
import telebot
from telebot import types
import requests
import json
#
bot = telebot.TeleBot('7496427449:AAH3vvZt4G36lHzWOiVz3nlhf5K1xsMQgAk')

# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     button_a = types.KeyboardButton("Кнопка A")
#     button_b = types.KeyboardButton("Кнопка B")
#     markup.add(button_a, button_b)
#
#     bot.send_message(message.chat.id, "Выберите кнопку", reply_markup=markup)
#
#
# @bot.message_handler(content_types=['text'])
# def handle_text(message):
#     A = list()
#     B = list()
#     if message.text == 'Кнопка A':
#         A.append(message.text)
#         bot.reply_to(message, f"Вы нажали кнопку {message.text}")
#     elif message.text == 'Кнопка B':
#         B.append(message.text)
#         bot.reply_to(message, f"Вы нажали кнопку {message.text}")
#
@bot.message_handler(commands=['поиск'])
def search(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_a = types.KeyboardButton("Найти город")
    markup.add(button_a)

    bot.send_message(message.chat.id, "Введите город", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    if message.text == 'Найти город':
        city = message.text
        url = 'https://vuzopedia-api.ru/search?q=' + city
        response = requests.get(url)
        data = response.json()
        bot.reply_to(message, f"В {city} есть следующие вузы:")
        for item in data['items']:
            bot.reply_to(message, item['name'])
bot.polling()