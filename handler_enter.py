import os
import numpy

from telegram import ReplyKeyboardRemove, User
import face_recognition

from db import db_session
from models import User
from keyboard import keyboard_enter


def examination_user(update, context):
    user_id = update.message.from_user.id
    user = db_session.query(User).filter(User.telegram_id == user_id).first()
    print(user.check_photo, user.in_active)
    
    if user.check_photo == True:
        update.message.reply_text(f"Для верификации загрузите вашу фотографию!", reply_markup=ReplyKeyboardRemove())
        return "examination_photo"
    else:
        update.message.reply_text(f"Ваша заявка обрабатывается!", reply_markup=keyboard_enter())


def examination_photo(update, context):
    os.makedirs('static/check_photo', exist_ok=True)  #создает папку текущей директории, если она уже существует, строка просто завершит работу.
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    user_id = update.message.from_user.id
    file_name = os.path.join('static/check_photo', f"{user_id}.jpg")
    photo_file.download(file_name)

    try:
        image = face_recognition.load_image_file(f"static/check_photo/{user_id}.jpg")
        biden_image = face_recognition.face_encodings(image)[0]
        user = db_session.query(User).filter(User.telegram_id == user_id).first()
        update.message.reply_text(
            "Фотография загружена, идет индентификация")
        if user.vector_photo == numpy.array2string(biden_image):
            update.message.reply_text(
            "Регистрация прошла успешно")

        else:
            update.message.reply_text(
                "Пользователь с данной биаметрией отсуствует")
    except IndexError:
        os.remove(f"check_photo/{user_id}.jpg")
        update.message.reply_text("Лицо не распознано! Загрузите другую фотографию")
        return "examination_photo"
