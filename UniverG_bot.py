# подключаем модуль для Телеграма

import telebot
import requests
from telebot import types
from selenium import webdriver
from bs4 import BeautifulSoup
from transliterate import translit
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler, Application

# указываем токен для доступа к боту
bot = telebot.TeleBot('7496427449:AAH3vvZt4G36lHzWOiVz3nlhf5K1xsMQgAk')


#  текст
start_txt = 'Привет! Это бот, который поможет тебе поступить в Университет! \n\nОтправьте боту название города, в который вы хотите поступить!'
next_txt = 'Выбирете предметы по которым вы сдавали ЕГЭ!'
pusto_txt = 'Вы ввели город , которого нет у нас в базе , либо же написали его неправильно. \n\nОтправьте боту снова название города , в который хотите поступить.'
net_vuzov_txt = 'По данной комбинации предметов в выбранном вами городе нет подходящих вузов. \n\n Выберите другую комбинациу предметов!'

linkG = []
univer_po_gor = list()
# обрабатываем старт бота
@bot.message_handler(commands=['start'])
def start(message):
    # выводим приветственное сообщение
    bot.send_message(message.from_user.id, start_txt, parse_mode='Markdown')

@bot.message_handler(content_types=['text'])
def univer(message):
    # получаем город из сообщения пользователя
    city = message.text
    city = translit(city, 'ru', reversed=True)

    if ' ' in city:
        city = city.split()
        city1 = ''
        for slov in city:
            if "'" == slov[-1]:
                slov = slov.replace("'", '')
            if 'ij' in slov:
                if 'ij' == slov[-2:]:
                    slov = slov.replace('ij', 'y')
                else:
                    slov = slov.replace('j', 'y')
            city1 += slov + '-'
        city = city1[:-1]
    if '-' in city:
        city = city.split('-')
        city1 = ''
        for slov in city:
            if "'" == slov[-1]:
                slov = slov.replace("'", '')
            if 'ij' in slov:
                if 'ij' == slov[-2:]:
                    slov = slov.replace('ij', 'y')
                else:
                    slov = slov.replace('j', 'y')
            city1 += slov + '-'
        city = city1[:-1]
    if 'ij' in city:
        if 'ij' == city[-2:]:
            city = city.replace('ij','y')
        else:
            city = city.replace('j','y')


    if "'j"  in city:
        city = city.replace("'j" ,'y')

    if "Ju"  in city:
        city = city.replace("Ju" ,'yu')
    if "ju"  in city:
        city = city.replace("ju" ,'yu')

    if "'" == city[-1]:
        city = city.replace("'", '')

    if 'Ja' in city:
        city = city.replace("Ja", 'ya')
    if 'ja' in city:
        city = city.replace("ja", 'ya')

    if "'" in city:
        city = city.replace("'", '')

    if "h" in city:
        city = city.replace("h", "kh")

    if 'zkh' in city:
        city = city.replace('zkh', 'zh')

    if 'sckh' in city:
        city = city.replace('sckh', 'sh')
    url = 'https://vuzopedia.ru/' + 'city/' + city
    # формируем запрос
    print(url)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')  # находит все элементы a
    for link in links:
        link1 = link.get('href')
        if 'region' in link1:
            linkG.append(link1)
            print(link1)  # выводит атрибут href каждого элемента a
            break

    if len(links) == 0: # Проверка правильности Города
        bot.send_message(message.from_user.id, pusto_txt, parse_mode='Markdown')
    else:
        bot.send_message(message.from_user.id, next_txt, parse_mode='Markdown')
        keyboard = types.InlineKeyboardMarkup()
        glavkey = types.InlineKeyboardMarkup()

        key_math    = types.InlineKeyboardButton(text='Математика / math', callback_data='math')
        keyboard.add(key_math)
        key_rus     = types.InlineKeyboardButton(text='Русский язык / russian', callback_data='rus')
        keyboard.add(key_rus)
        key_fiz     = types.InlineKeyboardButton(text='Физика / physics', callback_data='fiz')
        keyboard.add(key_fiz)
        key_obsh     = types.InlineKeyboardButton(text='Обществознание / Social Studies', callback_data='obsh')
        keyboard.add(key_obsh)
        key_ist    = types.InlineKeyboardButton(text='История / History', callback_data='ist')
        keyboard.add(key_ist)
        key_inform    = types.InlineKeyboardButton(text='Информатика / Computer science', callback_data='inform')
        keyboard.add(key_inform)
        key_biol     = types.InlineKeyboardButton(text='Биология / Biology', callback_data='biol')
        keyboard.add(key_biol)
        key_him      = types.InlineKeyboardButton(text='Химия / Chemistry', callback_data='him')
        keyboard.add(key_him)
        key_georg    = types.InlineKeyboardButton(text='География / Geography', callback_data='georg')
        keyboard.add(key_georg)
        key_liter    = types.InlineKeyboardButton(text='Литература / Literature', callback_data='liter')
        keyboard.add(key_liter)
        key_inyaz    = types.InlineKeyboardButton(text='Иностранные языки / Foreign languages', callback_data='inyaz')
        keyboard.add(key_inyaz)
        key_vstup    = types.InlineKeyboardButton(text='Вступительные экзамены / Entrance exams', callback_data='vstup')
        keyboard.add(key_vstup)
        bot.send_message(message.chat.id, "Выберите предметы", reply_markup=keyboard)

        key_univer = types.InlineKeyboardButton(text='Найти Университеты', callback_data='univer')
        glavkey.add(key_univer)

        bot.send_message(message.chat.id, "После выбора предметов нажмите на кнопку", reply_markup=glavkey)

predmets = list()

def callback_worker(call):
    if call.data == "math":
        predmets.append('mat')
    elif call.data == "rus":
        predmets.append('rus')
    elif call.data == "fiz":
        predmets.append('fiz')
    elif call.data == "obsh":
        predmets.append('obsh')
    elif call.data == "ist":
        predmets.append('ist')
    elif call.data == "inform":
        predmets.append('inform')
    elif call.data == "biol":
        predmets.append('biol')
    elif call.data == "him":
        predmets.append('him')
    elif call.data == "georg":
        predmets.append('georg')
    elif call.data == "liter":
        predmets.append('liter')
    elif call.data == "inyaz":
        predmets.append('inyaz')
    elif call.data == "vstup":
        predmets.append('vstup')
    elif call.data == "univer":
        unique_fruits = list(set(predmets))
        print(unique_fruits)
        result = ""
        region = ""
        for item in unique_fruits:
            result += 'ege' + item + ';'
        for item in linkG:
            region += item
        if 'egevstup' in result:
            result = result.replace('egevstup', 'vstup')
        print(result)
        print(linkG)
        url = 'https://vuzopedia.ru' + region + '/poege/' + result
        # обновление функции , которая отвечает за число города

        region = ''

        print(url[:-1])



        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # отслеживаю количество страниц на сайте , чтобы понять : нужно ли проверять другие страницы сайта с подходящими университетами

        pages = soup.find_all('li', class_='pagination')

        for page in pages:
            number_of_pages = page.text
            print(number_of_pages)

        # отслеживаю университеты на странице , полученной из данных пользователя

        univers = soup.find_all('div', class_='itemVuzTitle')
        for item in univers:
            title = item.text
            univer_po_gor.append(title)
            print(title)



        # отслеживаю количество страниц на сайте , чтобы понять : нужно ли проверять другие страницы сайта с подходящими университетами

        keyboard = types.InlineKeyboardMarkup()

        pages = soup.find_all('li', class_='pagination')

        for page in pages:
            number_of_pages = page.text
            print(number_of_pages)

        if len(univers) == 0:
            bot.send_message(call.from_user.id,net_vuzov_txt , parse_mode='Markdown')
        else:
            for vuz in univer_po_gor:
                #bot.send_message(call.from_user.id, vuz, parse_mode='Markdown')

                vuz_num = soup.find_all('li', class_='pagination')
                key_vuzs = types.InlineKeyboardButton(vuz,callback_data='vstup')
                keyboard.add(key_vuzs)
            bot.send_message(call.from_user.id, "Вот вузы , которые я нашел", reply_markup=keyboard)
            result = ""
            region = ""
        unique_fruits = ""


bot.polling(none_stop=True, interval=0)