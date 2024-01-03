from enum import Enum

from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from storage import storage
from utils.user_formats import UserFormats

CMD = "remove_user"

REMOVE_USER_CB_CONDITION = "- "
CB_LAMBDA = lambda call : call.data[:len(REMOVE_USER_CB_CONDITION)] == REMOVE_USER_CB_CONDITION
DATA_FROM_CB = lambda call: call.data[len(REMOVE_USER_CB_CONDITION):] 

class RemoveUserMessages(Enum):
    COMMAND_HEAD =          "Select a user to remove.\nTo edit the admin user see the code documentation."
    BUTTON_CANCEL =         "❌ Cancel"
    BUTTON_CANCEL_CB_DATA = "CANCEL"

    SUCCESS =   "✅ User %(user_id)s has been removed!"
    ERROR =     "❌ Cannot remove user %(user_id)s"

    def set_user(self, user_id):
        if self == RemoveUserMessages.SUCCESS or self == RemoveUserMessages.ERROR:
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
            RemoveUserMessages.BUTTON_CANCEL.value,
            callback_data=build_cb_data(RemoveUserMessages.BUTTON_CANCEL_CB_DATA.value)
        )
    )
    
    return markup


def handle_user_remove(message, bot):

    bot.send_message(
        message.chat.id,
        RemoveUserMessages.COMMAND_HEAD.value,
        reply_markup = get_task_markup()
    )


def user_remove_selection_cb(call, bot):

    bot.answer_callback_query(call.id, "")

    if DATA_FROM_CB(call) == RemoveUserMessages.BUTTON_CANCEL_CB_DATA.value:
        bot.send_message(call.message.chat.id, "Cancelled")
        
    else:
        user_to_remove = int(DATA_FROM_CB(call))

        result = storage.remove_user(user_to_remove)

        if result.is_success:
            bot.send_message(
                call.message.chat.id,
                RemoveUserMessages.SUCCESS.set_user(user_to_remove)
            )
        else:

            bot.send_message(
                call.message.chat.id,
                RemoveUserMessages.ERROR.set_user(user_to_remove) + "\nReason: " + result.message
            )
    