import logging
from multiprocessing import context
import os
import numpy

from dotenv import load_dotenv
from numpy import delete
from sqlalchemy import create_engine, engine_from_config, exists, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, User
import face_recognition
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from db import db_session
from models import User
import psycopg2
from psycopg2.errors import UniqueViolation
from psycopg2 import errors
from sqlalchemy.exc import IntegrityError


logging.basicConfig(filename="bot.log", level=logging.INFO)


def keyboard_registration():
    return ReplyKeyboardMarkup([["Регистрация", "Вход"]], resize_keyboard=True)


def start(update, context):
    print("Вызван /start")
    update.message.reply_text(f"Привет! Для прохождения верификации нажми Вход или зарегистрируйся.",
                              reply_markup=keyboard_registration())


class BadRequest(Exception):
    pass


def start_registration(update, context):
    user_id = update.message.from_user.id
    #exist = db_session.query(exists().where(User.telegram_id == user_id)).scalar()


    if User.telegram_id == user_id:
        user = User(
            username=update.message.from_user.name,
            telegram_id=update.message.from_user.id,
            check_photo=False,
            in_active=False,
            name='0'
        )
        db_session.add(user)
        db_session.commit()
        update.message.reply_text(f"Напишите ваше имя!", reply_markup=ReplyKeyboardRemove())
        return "name"
    else:
        update.message.reply_text(f"Вы уже заполнили анкету, вашу заявку обрабатывают!")
        return keyboard_registration


def name_registration(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.text                           
    user = db_session.query(User).filter(User.telegram_id == user_id).first()
    user.name = user_name
    db_session.commit()
    update.message.reply_text("Вставьте вашу фотографию!")
    return "photo"


def photo_registration(update, context):
    update.message.reply_text("Обрабатываем вашу фотографию!")
    
    os.makedirs('downloads', exist_ok=True) #создает папку текущей директории, если она уже существует, строка просто завершит работу.
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    user_id = update.message.from_user.id
    file_name = os.path.join('downloads', f"{user_id}.jpg")
    photo_file.download(file_name)

    try:
        image = face_recognition.load_image_file(f"downloads/{user_id}.jpg")
        biden_image = face_recognition.face_encodings(image)[0]
        print(biden_image)
        user = db_session.query(User).filter(User.telegram_id == user_id).first()
        user.vector_photo = numpy.array2string(biden_image)
        db_session.commit()
        update.message.reply_text(
            "Файл сохранен!",
            reply_markup=keyboard_registration()
        )
    except IndexError:
        os.remove(f"downloads/{user_id}.jpg")
        update.message.reply_text("Лицо не распознано! Загрузите другую фотографию")
        return "photo"



def user_enter(update, context):
    update.message.reply_text(
        "Для верификации необходимо прислать вашу фотографию!",
        reply_markup=ReplyKeyboardRemove())
    return update.message.reply_text("Файл сохранен!")


def photo_verification(update, context):
    pass


def main():
    load_dotenv() # будет искать файл .env, и, если он его найдет

    bot_api = os.getenv("bot_api")
    mybot = Updater(os.getenv("bot_api"), use_context=True)

    dp = mybot.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    registration_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("^(Регистрация)$"),
                      start_registration)],
        states={
            "name": [MessageHandler(Filters.text, name_registration)],
            "photo": [MessageHandler(Filters.photo, photo_registration)]
        },
        fallbacks=[]
    )
    enter_handler = ConversationHandler(
        entry_points=[dp.add_handler(MessageHandler(Filters.regex("^(Вход)$"), user_enter))],
        states ={
            "enter": [MessageHandler(Filters.photo, photo_verification)]
        },
        fallbacks=[]
    )

    dp.add_handler(registration_handler)
    dp.add_handler(enter_handler)
    
    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
