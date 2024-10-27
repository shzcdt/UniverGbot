from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import CallbackContext, CallbackQueryHandler, CommandHandler, ConversationHandler, Application, \
    MessageHandler, filters
import requests
import telebot
from telebot import types
from selenium import webdriver
from bs4 import BeautifulSoup
from transliterate import translit

TASK_CHOICE, VUZ_FIND, FAC_VUZ, VUZ_GOROD_PROMPT, PREDMETS, VUZ_PO_STR = range(
    6,
)

#  текст

next_txt = 'Выберите предметы по которым вы сдавали ЕГЭ!'
pusto_txt = 'Вы ввели город , которого нет у нас в базе , либо же написали его неправильно. \n\nОтправьте боту снова название города , в который хотите поступить.'
net_vuzov_txt = 'По данной комбинации предметов в выбранном вами городе нет подходящих вузов. \n\n Выберите другую комбинациу предметов!'

CALLBACK_QUERY_ARG = "update.callback_query"
MESSAGE_ARG = "update.message"


def univer(message):
    # получаем город из сообщения пользователя
    city = message
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
            city = city.replace('ij', 'y')
        else:
            city = city.replace('j', 'y')

    if "'j" in city:
        city = city.replace("'j", 'y')

    if "Ju" in city:
        city = city.replace("Ju", 'yu')
    if "ju" in city:
        city = city.replace("ju", 'yu')

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
    print(url)
    # формируем запрос
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all('a')  # находит все элементы a
    for link in links:
        link1 = link.get('href')
        if 'region' in link1:
            return link1
    if len(links) == 0:  # Проверка правильности Города
        return 1

def create_predmet_keyboard(predmets):
    if 'mat' in predmets:
        math = "V"
    else:
        math = "X"

    if 'rus' in predmets:
        rus = "V"
    else:
        rus = "X"

    if 'fiz' in predmets:
        fiz = "V"
    else:
        fiz = "X"

    if 'obsh' in predmets:
        obsh = "V"
    else:
        obsh = "X"

    if 'ist' in predmets:
        ist = "V"
    else:
        ist = "X"

    if 'inform' in predmets:
        inform = "V"
    else:
        inform = "X"

    if 'biol' in predmets:
        biol = "V"
    else:
        biol = "X"

    if 'him' in predmets:
        him = "V"
    else:
        him = "X"

    if 'georg' in predmets:
        georg = "V"
    else:
        georg = "X"

    if 'liter' in predmets:
        liter = "V"
    else:
        liter = "X"

    if 'inyaz' in predmets:
        inyaz = "V"
    else:
        inyaz = "X"

    if 'vstup' in predmets:
        vstup = "V"
    else:
        vstup = "X"


    keyboard = [
        [InlineKeyboardButton("Математика / math - {}".format(math), callback_data="mat")],
        [InlineKeyboardButton("Русский язык / russian - {}".format(rus), callback_data="rus")],
        [InlineKeyboardButton("Физика / physics - {}".format(fiz), callback_data="fiz")],
        [InlineKeyboardButton("Обществознание / Social Studies - {}".format(obsh), callback_data="obsh")],
        [InlineKeyboardButton("История / History - {}".format(ist), callback_data="ist")],
        [InlineKeyboardButton("Информатика / Computer science - {}".format(inform), callback_data="inform")],
        [InlineKeyboardButton("Биология / Biology - {}".format(biol), callback_data="biol")],
        [InlineKeyboardButton("Химия / Chemistry - {}".format(him), callback_data="him")],
        [InlineKeyboardButton("География / Geography - {}".format(georg), callback_data="georg")],
        [InlineKeyboardButton("Литература / Literature - {}".format(liter), callback_data="liter")],
        [InlineKeyboardButton("Иностранные языки / Foreign languages - {}".format(inyaz), callback_data="inyaz")],
        [InlineKeyboardButton("Вступительные экзамены / Entrance exams - {}".format(vstup), callback_data="vstup")],
    ]
    if len(predmets) != 0:
        key_univer = [InlineKeyboardButton("✅Найти Университеты✅", callback_data="find_univer")]
        keyboard.append(key_univer)
    return InlineKeyboardMarkup(keyboard)

def create_vuz_keyboard(url):
    print(url)
    response1 = requests.get(url)
    response2 = requests.get(url[:-1] + str(int(url[-1:]) + 1))
    soup1 = BeautifulSoup(response1.text, 'html.parser')
    soup2 = BeautifulSoup(response2.text, 'html.parser')
    # div = soup.find('div', class_='col-md-7 blockAfter')
    # number_of_univer = [x.text for x in div.find_all('a href')]
    univer_po_gor = [x.text for x in soup1.find_all('div', class_='itemVuzTitle')]
    univers_po_gor = [x.text for x in soup2.find_all('div', class_='itemVuzTitle')]
    print(univer_po_gor)
    keyboard = []
    if len(univers_po_gor) != 0 and univers_po_gor != univer_po_gor:
        keyboard.append([InlineKeyboardButton("XXXX Следующая страница XXXX", callback_data="next")])
    for item in univer_po_gor:
        keyboard.append([InlineKeyboardButton(item[21:-16], callback_data="hz")])
    if url[-2:] != '=1':
        keyboard.append([InlineKeyboardButton("XXXX Предыдущая страница XXXX", callback_data="back")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, _: CallbackContext) -> int:
    """Начальный хэндлер дерева команд."""
    keyboard = [
        [InlineKeyboardButton("Найти университет", callback_data="VUZ_FIND")],
        [InlineKeyboardButton("Определить факультет в нужном тебе вузе", callback_data="FAC_VUZ")],
        [InlineKeyboardButton("Узнать возможность поступить на какой-либо факультет", callback_data="FAC_CHANSE")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    if update.message:  # When /start command is used
        await update.message.reply_text("Выберите задачу:", reply_markup=reply_markup)
    elif update.callback_query:
        await update.callback_query.edit_message_text("Выберите задачу:", reply_markup=reply_markup)
    return TASK_CHOICE


async def task_choice(update: Update, _: CallbackContext) -> int:
    """хэндлер выбора базовой группы задач."""
    query = update.callback_query
    if query is None:
        raise Exception(CALLBACK_QUERY_ARG)
    await query.answer()
    choice = query.data
    if choice == "VUZ_FIND":
        # будет находиться основой код для поиска вуза

        keyboard = [
            [InlineKeyboardButton("Поиск вуза по городу", callback_data="VUZ_GOROD")],
            [InlineKeyboardButton("Назад", callback_data="BACK")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text="Ты выбрал найти университет:", reply_markup=reply_markup)
        return VUZ_FIND
    if choice == "FAC_VUZ":
        # будет находиться код , для поиска факультета по вузу
        # reply_markup = InlineKeyboardMarkup(keyboard)
        # await query.edit_message_text(text="Помощь в решении задачи:", reply_markup=reply_markup)
        return FAC_VUZ
    if choice == "FAC_CHANSE":
        await update.callback_query.edit_message_text(text="Скоро мы научимся объяснять мемы. Беседа завершена.")
        return ConversationHandler.END
    raise Exception(choice)


async def vuz_find(update: Update, context: CallbackContext) -> int:
    """хэндлер выбора прокачки знаний."""

    query = update.callback_query
    if query is None:
        raise Exception(CALLBACK_QUERY_ARG)
    await query.answer()
    choice = query.data
    if choice == "VUZ_GOROD":
        await update.callback_query.edit_message_text(text="Впишите город ,в который хотите поступить:")
        return VUZ_GOROD_PROMPT
    if choice == "BACK":
        return await start(update, context)
    raise Exception(choice)


async def fac_vuz(update: Update, context: CallbackContext) -> int:
    """хэндлер выбора помощи в решении задач."""
    query = update.callback_query
    if query is None:
        raise Exception(CALLBACK_QUERY_ARG)
    await query.answer()
    choice = query.data

    if choice == "BACK":
        return await start(update, context)
    raise Exception(choice)


async def code_explanation(update: Update, _: CallbackContext) -> int:
    """Хэндлер выбора объяснения кода."""
    query = update.callback_query
    if query is None:
        raise Exception(CALLBACK_QUERY_ARG)

    await update.callback_query.edit_message_text(text="Скоро мы научимся объяснять код. Беседа завершена.")
    return ConversationHandler.END


async def cancel(update: Update, _: CallbackContext) -> int:
    """Завершает беседу."""
    if update.message is None:
        raise Exception(MESSAGE_ARG)
    await update.message.reply_text("Беседа завершена.", reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END

async def vuz_gorod_prompt(update: Update, context: CallbackContext) -> int:
    if update.message is None:
        raise Exception(MESSAGE_ARG)
    cont = update.message.text
    context.user_data["city"] = cont
    city = univer(cont)
    if city == 1:
        bot.send_message(update.effective_chat.id, pusto_txt, parse_mode='Markdown')
        return VUZ_GOROD_PROMPT
    print(city)
    context.user_data["region"] = city
    context.user_data["predmets"] = list()
    await update.message.reply_text("Выберите предметы:", reply_markup=create_predmet_keyboard(context.user_data["predmets"]))
    return PREDMETS

async def predmets_button(update: Update, context: CallbackContext) -> int:
    predmets: list = context.user_data["predmets"]
    if update.callback_query.data != 'find_univer':
        predmet = update.callback_query.data
        if predmet in predmets:
            predmets.remove(predmet)
        else:
            predmets.append(predmet)
            context.user_data["predmets"] = predmets
        await update.callback_query.edit_message_text(text="Загрузка...", reply_markup=create_predmet_keyboard(predmets))
        await update.callback_query.edit_message_text(text="Выберите предметы:", reply_markup=create_predmet_keyboard(predmets))
        return PREDMETS

    result = ''
    for item in predmets:
        result += 'ege' + item + ';'
    univer_po_gor = list()
    url = 'https://vuzopedia.ru' + context.user_data["region"] + '/poege/' + result + '?page='
    context.user_data["url"] = url

    num = 1
    context.user_data['num'] = num
    url = url + str(num)
    # Вывод клавиатурки с университетами
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    univer_po_gor = [x.text for x in soup.find_all('div', class_='itemVuzTitle')]
    if len(univer_po_gor) == 0:
        context.user_data["predmets"] = list()
        context.user_data["predmets"] = predmets
        await update.callback_query.edit_message_text(text="По данному набору нет университетов:",reply_markup=create_predmet_keyboard(predmets))
        return PREDMETS

    keyboard = create_vuz_keyboard(url)
    await update.callback_query.edit_message_text(text="Найденные университеты:\n\n Страница " + str(num), reply_markup=keyboard)
    return VUZ_PO_STR

async def vuz_po_str(update: Update, context: CallbackContext) -> int:
    num = context.user_data['num']
    url = context.user_data["url"]
    if update.callback_query.data == 'next':
        context.user_data['num'] += 1
        url = url + str(context.user_data['num'])
        keyboard = create_vuz_keyboard(url)
        await update.callback_query.edit_message_text(text="Найденные университеты:\n\n Страница " + str(context.user_data['num']), reply_markup=keyboard)
        return VUZ_PO_STR

    if update.callback_query.data == 'back':
        context.user_data['num'] -= 1
        url = url + str(context.user_data['num'])
        keyboard = create_vuz_keyboard(url)
        await update.callback_query.edit_message_text(text="Найденные университеты:\n\n Страница " + str(context.user_data['num']), reply_markup=keyboard)
        return VUZ_PO_STR
    return ConversationHandler.END

"""Run the bot."""
conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        TASK_CHOICE: [CallbackQueryHandler(task_choice)],
        VUZ_FIND: [CallbackQueryHandler(vuz_find)],
        FAC_VUZ: [CallbackQueryHandler(fac_vuz)],
        VUZ_GOROD_PROMPT: [MessageHandler(filters.TEXT & ~filters.COMMAND, vuz_gorod_prompt)],
        PREDMETS: [CallbackQueryHandler(predmets_button)],
        VUZ_PO_STR: [CallbackQueryHandler(vuz_po_str)]
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)

bot = telebot.TeleBot('7470512616:AAG7WIJyJp4KaYMvA-xgd0_2g2a_q_iHoW0')
application: Application = Application.builder().token("7470512616:AAG7WIJyJp4KaYMvA-xgd0_2g2a_q_iHoW0").build()

application.add_handler(conv_handler)
application.add_handler(CommandHandler("start", start))

application.run_polling()
