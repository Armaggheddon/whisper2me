from enum import Enum
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from storage import storage

CMD = "add_user"

class Messages(Enum):
    COMMAND_INFO =      "Send the user_id of the user you want to add.\nYou can also forward the user's message"
    NOT_TEXT =  "❌ The user id MUST BE a text message!"
    USER_ID_TOO_SHORT = "❌ The user ID has at most 10 digits!"
    USER_ID_NOT_NUMBER = "❌ The user ID must be a number!"

    SUCCESS =           "✅ User %(user_id)s has been added!"
    ERROR =             "❌ User %(user_id)s is already allowed"

    def set_user(self, user_id):
        '''Sets the user id in the message
        
        Args:
        - user_id - the user id to set
        '''
        return self.value % {"user_id" : str(user_id)}



def handle_user_id(message, bot):
    
    if message.content_type != "text":
        bot.send_message(
            message.chat.id,
            Messages.NOT_TEXT.value
        )
        return

    user_to_add = message.text
    
    # Support the scenario where the id is taken from a forwarded message
    # to avoid "walkaround methods" to obtain the user_id
    if message.forward_from != None:
        user_to_add = message.forward_from.id

    else:
        if len(user_to_add) > 10:
            
            bot.send_message(
                message.chat.id,
                Messages.USER_ID_TOO_SHORT.value
            )
            return
    
    try:
        
        if type(user_to_add) is not int:
            user_to_add = int(user_to_add)

        result = storage.add_user(user_to_add)

        if result.is_success:
            bot.send_message(
                message.chat.id,
                Messages.SUCCESS.set_user(user_to_add)
            )
        else:
            bot.send_message(
                message.chat.id,
                Messages.ERROR.set_user(user_to_add) + f"\n\nReason: {result.message}"
            )

    except ValueError:
        bot.send_message(
            message.chat.id,
            Messages.USER_ID_NOT_NUMBER.value
        )


def handle_user_add(message, bot):

    bot.send_message(
        message.chat.id,
        Messages.COMMAND_INFO.value
    )

    bot.register_next_step_handler(message, handle_user_id, bot)
