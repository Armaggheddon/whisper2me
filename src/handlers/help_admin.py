from enum import Enum

from telebot import TeleBot
from telebot.types import Message

CMD = "help"

class Messages(Enum):
    HELP = (
        "Available commands 📒: \n\n"
        "/start  starts the bot\n"
        "/language  change the target language for the transcription for all users\n"
        "/task  change the task to perform for all users\n"
        "/add_user  allow a new user to use the bot\n"
        "/remove_user  remove an existing user\n"
        "/users  list the currently allowed users\n"
        "/purge  remove all existing users\n"
        "/help  shows this message\n\n"
        "To use the bot simply forward a voice message!"
    )

def handle_admin_help_command(message : Message, bot : TeleBot):

    bot.send_message(
        message.chat.id,
        Messages.HELP.value
    )
