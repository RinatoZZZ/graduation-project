import os
import numpy

from dotenv import load_dotenv
from numpy import delete
from sqlalchemy import create_engine, engine_from_config, exists, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from telegram import  ReplyKeyboardRemove, User
import face_recognition
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from db import db_session
from models import User
from keyboard import keyboard_registration, keyboard_enter


def start_registration(update, context):
    user_id = update.message.from_user.id
    exist = db_session.query(exists().where(User.telegram_id == user_id)).scalar()

    if exist == False:
        user = User(
            username=update.message.from_user.name,
            telegram_id=update.message.from_user.id,
            check_photo=False,
            in_active=False,
            name='0'
        )
        db_session.add(user)
        db_session.commit()
        update.message.reply_text(f"Напишите ваше имя!", 
                                reply_markup=ReplyKeyboardRemove())
        return "name"
    else:
        update.message.reply_text(f"Вы уже заполнили анкету, вашу заявку обрабатывают!",
                                reply_markup=keyboard_enter()
        )


def name_registration(update, context):
    user_id = update.message.from_user.id
    user_name = update.message.text                           
    user = db_session.query(User).filter(User.telegram_id == user_id).first()
    user.name = user_name
    db_session.commit()
    update.message.reply_text("Загрузите вашу фотографию!")
    return "photo"


def photo_registration(update, context):
    update.message.reply_text("Обрабатываем вашу фотографию!")
    
    os.makedirs('static/user_photo', exist_ok=True)  #создает папку текущей директории, если она уже существует, строка просто завершит работу.
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    user_id = update.message.from_user.id
    file_name = os.path.join('static/user_photo', f"{user_id}.jpg")
    photo_file.download(file_name)

    try:
        image = face_recognition.load_image_file(f"static/user_photo/{user_id}.jpg")
        biden_image = face_recognition.face_encodings(image)[0]
        user = db_session.query(User).filter(User.telegram_id == user_id).first()
        user.vector_photo = numpy.array2string(biden_image)
        db_session.commit()
        update.message.reply_text(
            "Файл сохранен!",
            reply_markup=keyboard_enter()
        )
    except IndexError:
        os.remove(f"check_photo/{user_id}.jpg")
        update.message.reply_text("Лицо не распознано! Загрузите другую фотографию")
        return "photo"
