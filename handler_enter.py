from copyreg import pickle
import os
import pickle
import base64
from datetime import datetime

from telegram import ReplyKeyboardRemove, User
import face_recognition

from db import db_session
from models import User
from keyboard import keyboard_enter
from checking_metadata import check_time_photo


def examination_user(update, context):
    user_id = update.message.from_user.id
    user = db_session.query(User).filter(User.telegram_id == user_id).first()
    if user.check_photo == True:
        update.message.reply_text(f"Для верификации загрузите вашу фотографию!", reply_markup=ReplyKeyboardRemove())
        return "photo_ver"
    else:
        update.message.reply_text(f"Ваша заявка обрабатывается!",
                                  reply_markup=keyboard_enter())


def examination_photo(update, context):
    update.message.reply_text(
            "Фотография загружена, идет индентификация")
    os.makedirs('static/check_photo', exist_ok=True)
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    user_id = update.message.from_user.id
    file_name = os.path.join('static/check_photo', f"{user_id}.jpg")
    photo_file.download(file_name)

    try:
        image = face_recognition.load_image_file(f"static/check_photo/{user_id}.jpg")
        unknown_vector = face_recognition.face_encodings(image)[0]
        user = db_session.query(User).filter(User.telegram_id == user_id).first()
        vector = pickle.loads(base64.b64decode((user.vector_photo).encode()))
        results_identification = face_recognition.compare_faces([vector], unknown_vector)
        print(results_identification)
        if results_identification[0] == True:
            update.message.reply_text("Регистрация прошла успешно", reply_markup=keyboard_enter())
        else:
            os.remove(f"static/check_photo//{user_id}.jpg")
            update.message.reply_text(
                    "Пользователь с данной биаметрией отсуствует", reply_markup=keyboard_enter())
    except IndexError:
        os.remove(f"static/check_photo//{user_id}.jpg")
        update.message.reply_text("Лицо не распознано! Загрузите другую фотографию")
        return "photo_ver"
