from enum import Enum

from telebot import TeleBot
from telebot.types import Message

CMD = "help"

class Messages(Enum):
    HELP = (
        "Available commands 📒: \n\n"
        "/start  starts the bot\n"
        "/help  shows this message\n\n"
        "To use the bot simply forward a voice message!"
    )

def handle_user_help_command(message : Message, bot : TeleBot):

    bot.send_message(
        message.chat.id,
        Messages.HELP.value
    )
