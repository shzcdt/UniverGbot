import telebot
from telebot import types
from telebot.types import Message
from aiogram import Bot, Dispatcher, executor, types

# Инициализация бота
bot = telebot.TeleBot("YOUR_TOKEN")

# Создание ConversationHandler
conversation_handler = ConversationHandler(
    entry_points=[CommandHandler('start', start)],
    states={
        'start': [MessageHandler(Filters.text & ~Filters.command, start_message),
                  CallbackQueryHandler(start_callback)]
    },
    fallbacks=[CommandHandler('help', help_message)]
)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(chat_id=message.chat.id, text="Привет! Как дела?")

@bot.message_handler()
def start_message(message):
    if message.text == 'Хорошо':
        bot.send_message(chat_id=message.chat.id, text='Отлично, у меня тоже всё хорошо!')

@bot.callback_query_handler(func=lambda call: True)
def start_callback(call):
    bot.answer_callback_query(call.id)
    bot.send_message(chat_id=call.message.chat.id, text='Что ты хочешь узнать?')

