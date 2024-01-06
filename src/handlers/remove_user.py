from enum import Enum

from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from storage import storage
from utils.user_formats import UserFormats

CMD = "remove_user"

# Callback data for user removal is "- <user_id>" where "-" if followed by a space
REMOVE_USER_CB_CONDITION = "- "
CB_LAMBDA = lambda call : call.data[:len(REMOVE_USER_CB_CONDITION)] == REMOVE_USER_CB_CONDITION
DATA_FROM_CB = lambda call: call.data[len(REMOVE_USER_CB_CONDITION):] 

class Messages(Enum):
    COMMAND_HEAD =          "Select a user to remove.\nTo edit the admin user see the code documentation."
    BUTTON_CANCEL =         "❌ Cancel"
    BUTTON_CANCEL_CB_DATA = "CANCEL"

    SUCCESS =   "✅ User %(user_id)s has been removed!"
    ERROR =     "❌ Cannot remove user %(user_id)s"

    def set_user(self, user_id):
        if self == Messages.SUCCESS or self == Messages.ERROR:
            return self.value % {"user_id" : str(user_id)}
        

def build_cb_data(data):
    return f"{REMOVE_USER_CB_CONDITION}{data}"

def get_task_markup():

    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    for user in storage.allowed_users:

        markup.add(
            InlineKeyboardButton(
                UserFormats.USER_NORMAL.set_user(user),
                callback_data = build_cb_data(user)
            )
        )
    
    markup.add(
        InlineKeyboardButton(
            Messages.BUTTON_CANCEL.value,
            callback_data=build_cb_data(Messages.BUTTON_CANCEL_CB_DATA.value)
        )
    )
    
    return markup


def handle_user_remove(message, bot):

    bot.send_message(
        message.chat.id,
        Messages.COMMAND_HEAD.value,
        reply_markup = get_task_markup()
    )


def user_remove_selection_cb(call, bot):

    bot.answer_callback_query(call.id, "")

    data = DATA_FROM_CB(call)

    if data == Messages.BUTTON_CANCEL_CB_DATA.value:
        bot.send_message(
            call.message.chat.id, 
            Messages.BUTTON_CANCEL.value
        )
        
    else:
        user_to_remove = int(data)

        result = storage.remove_user(user_to_remove)

        if result.is_success:
            bot.send_message(
                call.message.chat.id,
                Messages.SUCCESS.set_user(user_to_remove)
            )
        else:

            bot.send_message(
                call.message.chat.id,
                Messages.ERROR.set_user(user_to_remove) + "\nReason: " + result.message
            )
    
    # Remove markup for buttons and delete language selection message
    # Remains only the response of the selection
    bot.edit_message_reply_markup(
        chat_id = call.message.chat.id,
        message_id = call.message.id,
        reply_markup=""
    )
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.id
    )

    bot.answer_callback_query(call.id, "")
    