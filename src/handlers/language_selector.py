from enum import Enum
from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from whisper_helper.languages import Languages, LanguagesDescription, LANGUAGE_KEY
from whisper_helper import _WhisperHelper


CMD = "language"

SELECT_LANGUAGE_CB_PREFIX = "L "
CB_LAMBDA = lambda call: call.data[:len(SELECT_LANGUAGE_CB_PREFIX)] == SELECT_LANGUAGE_CB_PREFIX
DATA_FROM_CB = lambda call : call.data[len(SELECT_LANGUAGE_CB_PREFIX):]


class Messages(Enum):
    COMMAND_HEAD = "Select language:"
    BUTTON_CANCEL = "❌ Cancel"
    BUTTON_CANCEL_CB_DATA = "CANCEL"
    
    LANGUAGE_SET_TO = "Language set to %(language)s"

    def with_language(self, language):
        if self != Messages.LANGUAGE_SET_TO:
            return self.value
        
        return self.value % {"language" : str(language)}


def build_cb_data(data):
    return f"{SELECT_LANGUAGE_CB_PREFIX}{data}"

def get_language_markup():
    markup = InlineKeyboardMarkup(row_width = 2)
    
    buttons = [
        InlineKeyboardButton(
            str(LanguagesDescription[language.name]), 
            callback_data=build_cb_data(language.name)
        ) for language in Languages
    ]
    # adding buttons one by one breaks row_width and simply stacks them
    markup.add(*buttons) 
    
    markup.row(
        InlineKeyboardButton(
            Messages.BUTTON_CANCEL.value, 
            callback_data = build_cb_data(Messages.BUTTON_CANCEL_CB_DATA.value)
        )
    )
    
    return markup


def handle_language_command(message : Message, bot : TeleBot):
    bot.send_message(
        message.chat.id,
        Messages.COMMAND_HEAD.value,
        reply_markup = get_language_markup(),
    )


def language_selection_cb(call, bot : TeleBot):
    data = DATA_FROM_CB(call)

    if data == Messages.BUTTON_CANCEL_CB_DATA.value:
        bot.send_message(
            call.from_user.id, 
            Messages.BUTTON_CANCEL.value
        )
    
    else:
        _WhisperHelper().change_language(Languages[data])

        bot.send_message(
            call.from_user.id, 
            Messages.LANGUAGE_SET_TO.with_language(LanguagesDescription[data])
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