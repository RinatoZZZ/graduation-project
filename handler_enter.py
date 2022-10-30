import os
import numpy

from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)
from sqlalchemy import create_engine, engine_from_config, exists, false
from telegram import ReplyKeyboardRemove

from db import db_session
from models import User

def user_enter(update, context):
    update.message.reply_text(
        "Для верификации необходимо прислать вашу фотографию!",
        reply_markup=ReplyKeyboardRemove())
    return update.message.reply_text("Файл сохранен!")


def photo_verification(update, context):
    pass