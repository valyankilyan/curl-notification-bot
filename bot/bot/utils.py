
from models.user import get_user_by_tg_id, save_new_user
from .mytelebot import myTeleBot
from models.user import get_admins


botForUtil = None
def init_util_bot(bot: myTeleBot):
    global botForUtil
    botForUtil = bot

  
def admin_only(func):
    def wrapper(message):
        client = get_user_by_tg_id(message.from_user.id)
        if client is None or (not client.is_admin):
            botForUtil.send_message(message.chat.id, "You can't do it!")
            return
        return func(message)
    return wrapper

def sync_user(bot: myTeleBot, user_id: int, username: str):
    user = get_user_by_tg_id(user_id)
    if user is None:
        save_new_user(user_id, username)
        send_notification_to_admins(bot, username)


def send_notification_to_admins(bot: myTeleBot, new_user_username: str):
    admins = get_admins()
    for admin in admins:
        bot.send_message(admin.tg_id, f'New user - @{new_user_username}')

def authenticate(telegram_id: str, password: str):
    return True