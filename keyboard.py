from telegram import ReplyKeyboardMarkup
import face_recognition
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)



def keyboard_registration():
    return ReplyKeyboardMarkup([["Регистрация", "Вход"]], resize_keyboard=True)


def keyboard_start():
    return ReplyKeyboardMarkup([["Старт"]], resize_keyboard=True)


def keyboard_enter():
    return ReplyKeyboardMarkup([["Вход"]], resize_keyboard=True)