import config
import telebot
from telebot import apihelper
from telebot import types
import datetime
import os
import logging
logger = logging.getLogger('log')
logger.setLevel(logging.INFO)
fh = logging.FileHandler('someTestBot.log')
fh.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s | %(levelname)-7s | %(message)s")
fh.setFormatter(formatter)
logger.addHandler(fh)
 
### Прокси сервер
#apihelper.proxy = {'https':'socks5h://login:password@ip-host:port'}
#apihelper.proxy = {'https':'socks5h://98.162.96.52:4145'}
### Token telegram bot
bot = telebot.TeleBot('1308167835:AAFSOSFtCIcae5U_jLNTO3j_Snud6VHGiI0', threaded=True)
 
### Функция проверки авторизации
def autor(chatid):
     strid = str(chatid)
     for item in config.users:
         if item == strid:
             return True
     return False
### Клавиатура
keyboard1 = telebot.types.ReplyKeyboardMarkup()
keyboard1.row('Введите название:')
 
### Прием документов
@bot.message_handler(content_types=['document'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id
 
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
 
        src = '/home/sysadmin' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Пожалуй, я сохраню это")
    except Exception as e:
        bot.reply_to(message, e)
 
### Прием фото
@bot.message_handler(content_types=['photo'])
def handle_docs_photo(message):
    try:
        chat_id = message.chat.id
 
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
 
        src = '/home/sysadmin/' + file_info.file_path;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "Фото добавлено")
 
    except Exception as e:
        bot.reply_to(message, e)
 
@bot.message_handler(commands=['start'])
def start_message(message):
    if autor(message.chat.id):
        cid = message.chat.id
        message_text = message.text
        user_id = message.from_user.id
        user_name = message.from_user.first_name
        bot.send_message(message.chat.id, 'Привет, ' + user_name + ' Что тебе надо от меня, собака сутулая!', reply_markup=keyboard1)
        bot.send_sticker(message.chat.id, 'CAADAgAD6CQAAp7OCwABx40TskPHi3MWBA')
    else:
        bot.send_message(message.chat.id, 'Пшел вон отсюда. Твой ID: ' + str(message.chat.id))
        bot.send_sticker(message.chat.id, 'CAADAgADcQMAAkmH9Av0tmQ7QhjxLRYE')
 
bot.polling()