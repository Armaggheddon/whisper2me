from enum import Enum
from telebot import TeleBot
from telebot.types import Message

CMD = "start"

class Messages(Enum): 
    START_TEMPLATE = (""
        "Hi %(user_name)s 👋🤓,\n\n"
        "if you are annoyed by audio messages, this is the bot for you 😉.\n"
        "Simply forward the audio message you want to transcribe and you will "
        "receive a message with its content when it is ready 🎯\n"
        "Enjoy!!")
    
    def with_userid(self, user_name):
        return self.value % {"user_name" : user_name}

def handle_start_command(message : Message, bot : TeleBot):
    bot.send_message(
        message.chat.id,
        Messages.START_TEMPLATE.with_userid(message.from_user.first_name)
    )