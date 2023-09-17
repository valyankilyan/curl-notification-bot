from .mytelebot import myTeleBot
from .admin import setup_admin_commands
from .commands import setup_default_commands
from .callback import setup_callback_queries
from .utils import authenticate
from flask import Flask, request
import time


def init_bot(bot: myTeleBot):
    bot.remove_webhook()
    time.sleep(0.1)
    bot.logger.info("Bot initialized.")


def init_flask(bot: myTeleBot, app: Flask, listen: str, port: int):
    @app.route('/', methods=['GET', 'HEAD'])
    def index():
        return 'hey, howrudoing?'

    @app.route('/send_notification', methods=['POST'])
    def send_notification():
        data = request.get_json()
        text = data.get('text')
        telegram_id = data.get('telegram_id')
        telegram_password = data.get('telegram_password')

        if authenticate(telegram_id, telegram_password):
            send_telegram_notification(telegram_id, text)
            return 'Notification sent successfully'
        else:
            return 'Authentication failed', 401
        
    def send_telegram_notification(telegram_id: str, text: str):
        bot.send_message(telegram_id, text)

    app.run(host=listen,
            port=port,
            debug=True)


def init_message_handlers(bot: myTeleBot):
    setup_admin_commands(bot)
    setup_default_commands(bot)
    setup_callback_queries(bot)

