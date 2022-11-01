from telegram import ReplyKeyboardMarkup


def keyboard_registration():
    return ReplyKeyboardMarkup([["Регистрация", "Вход"]], resize_keyboard=True)


def keyboard_start():
    return ReplyKeyboardMarkup([["Старт"]], resize_keyboard=True)


def keyboard_enter():
    return ReplyKeyboardMarkup([["Вход"]], resize_keyboard=True)