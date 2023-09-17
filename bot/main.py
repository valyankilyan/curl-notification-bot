import threading
from bot.mytelebot import myTeleBot
from bot.bot import init_bot, init_message_handlers, init_flask
from logger.logger import getLogger
from bot.utils import init_util_bot
from flask import Flask
from config.bot import *

app = Flask(__name__)

if __name__ == "__main__":
    logger = getLogger(logging_config_path)

    logger.debug("reading config")

    bot = myTeleBot(token, logger)
    init_bot(bot)

    init_util_bot(bot)

    init_message_handlers(bot)

    def bot_thread_func():
        bot.polling(none_stop=True)
    bot_thread = threading.Thread(target=bot_thread_func)
    bot_thread.start()

    init_flask(bot, app, host, int(port))


