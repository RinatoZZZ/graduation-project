import logging
import os
from multiprocessing import context

from dotenv import load_dotenv
from sqlalchemy import create_engine, engine_from_config, exists, false
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, User
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from db import db_session
from models import User
import psycopg2
from psycopg2.errors import UniqueViolation
from sqlalchemy.exc import IntegrityError

from handler_enter import examination_user, examination_photo
from handler_registration import start_registration, name_registration, photo_registration
from keyboard import keyboard_registration


logging.basicConfig(filename="bot.log", level=logging.INFO)


def start(update, context):
    print("Вызван /start")
    update.message.reply_text(f"Привет! Для прохождения верификации нажми Вход или зарегистрируйся.",
                              reply_markup=keyboard_registration())


class BadRequest(Exception):
    pass


def cancel(update, context):
    return keyboard_registration


def main():
    load_dotenv() # будет искать файл .env, и, если он его найдет
    bot_api = os.getenv("bot_api")
    mybot = Updater(os.getenv("bot_api"), use_context=True)

    dp = mybot.dispatcher
    registration_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("^(Регистрация)$"),
                      start_registration)],
        states={
            "name": [MessageHandler(Filters.text, name_registration)],
            "photo": [MessageHandler(Filters.photo, photo_registration)]
        },
        fallbacks=[MessageHandler(Filters.regex("^(Выход)$"), cancel)]
    )

    enter_handler = ConversationHandler(
        entry_points=[MessageHandler(Filters.regex("^(Вход)$"),
                      examination_user)],
        states={
            "name": [MessageHandler(Filters.photo, examination_photo)],
        },
        fallbacks=[MessageHandler(Filters.regex("^(Выход)$"), cancel)]
    )


    dp.add_handler(CommandHandler("Start", start))
    dp.add_handler(registration_handler)
    dp.add_handler(enter_handler)


    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()
