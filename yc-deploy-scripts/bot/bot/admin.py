import os
from .utils import admin_only
from .mytelebot import myTeleBot
from models.user import *
from config.bot import admin_password

def setup_admin_commands(bot: myTeleBot):
    @bot.message_handler(commands=['become_admin'])
    def assign_admin(message):
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        callback = bot.send_message(message.chat.id, "Please enter the password to receive admin rights")
        bot.register_next_step_handler(callback, receive_password)

    def receive_password(message):
        if message.text == admin_password:
            user = get_user_by_tg_id(message.from_user.id)
            if user is not None:
                grant_user_admin_role(user)
                bot.logger.info(f'{message.from_user.username} received admin rights')
                bot.send_message(message.chat.id, "Now you're admin!")
        else:
            bot.send_message(message.chat.id, "Wrong password! Fuck off")
        bot.delete_message(message.chat.id, message.message_id)


    @bot.message_handler(commands=['users'])
    @admin_only
    def get_users(message):
        bot.logger.info(f'{message.from_user.username} sent {message.text}')
        users = get_users()
        out = "\n".join(map(repr, users))
        bot.send_message(message.chat.id, "Found users:\n" + out)

