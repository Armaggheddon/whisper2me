from enum import Enum
from telebot import TeleBot
from telebot.types import Message

from storage import UsersStorage

CMD = "purge"

class Messages(Enum):
    COMMAND_INFO = "⚠️⚠️ Are you sure you want to delete all users?\n\nType \"YES\" to continue"
    NOT_YES = "⚠️ The response must be YES in capital letters!"
    YES = "✅ All allowed users have been removed!"

def handle_purge_continuation(message, bot):

    if message.content_type != "text":
        bot.send_message(
            message.chat.id,
            Messages.NOT_YES.value
        )
        return
    
    response = message.text

    if response == "YES":
        
        result = UsersStorage.get_instance().purge_users()
        
        if result.is_success:
            bot.send_message(
                message.chat.id,
                Messages.YES.value
            )
        else:
            bot.send_message(
                message.chat.id,
                result.message
            )
    else:
        bot.send_message(
            message.chat.id,
            Messages.NOT_YES.value
        )



def handle_purge_command(message : Message, bot : TeleBot):
    
    bot.send_message(
        message.chat.id,
        Messages.COMMAND_INFO.value
    )

    bot.register_next_step_handler(message, handle_purge_continuation, bot)
