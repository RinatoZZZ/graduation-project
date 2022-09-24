import logging
from telegram.ext import Updater, messagehandler, commandhandler, Filters

logging.basicConfig(filename="bot.log", level=logging.INFO)


def main():
    mybot = Updater("5592454745:AAHNaS1r9EDKAyKL1VvkiB6QbnNYhIGwIeU", use_context=True)


    logging.info("Бот стартовал")
    mybot.start_polling()
    mybot.idle()


if __name__ == "__main__":
    main()