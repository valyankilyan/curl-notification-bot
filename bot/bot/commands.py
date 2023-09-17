from .mytelebot import myTeleBot
from models.user import *
from .answers import *
from models.user import *
from .utils import sync_user



def setup_default_commands(bot: myTeleBot):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        sync_user(bot, message.from_user.id, message.from_user.username)
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        bot.send_message(message.chat.id, start_text, parse_mode='Markdown', disable_web_page_preview=True)


    @bot.message_handler(commands=['help'])
    def send_help(message):
        sync_user(bot, message.from_user.id, message.from_user.username)
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        bot.send_message(message.chat.id, help_text, parse_mode='Markdown', disable_web_page_preview=True)


    @bot.message_handler(func=lambda m: True)
    def error(message):
        sync_user(bot, message.from_user.id, message.from_user.username)
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        bot.reply_to(message, "Error!")
