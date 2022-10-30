from telegram import ReplyKeyboardMarkup

def keyboard_registration():
    return ReplyKeyboardMarkup([["Регистрация", "Вход"]], resize_keyboard=True)


def keyboard_start():
    return ReplyKeyboardMarkup([["/Start"]], resize_keyboard=True)


def keyboard_enter():
    return ReplyKeyboardMarkup([["Вход"]], resize_keyboard=True)