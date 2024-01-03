from telebot import TeleBot
from telebot.types import Message, InlineKeyboardMarkup, InlineKeyboardButton

from whisper_helper.languages import Languages, LanguagesDescription, LANGUAGE_KEY
from whisper_helper import _WhisperHelper


CMD = "language"

CB_LAMBDA = lambda call: call.data in Languages.list_names()


def get_language_markup():
    markup = InlineKeyboardMarkup()
    markup.row_width = 2

    for language in Languages:
        markup.add(
            InlineKeyboardButton(
                str(LanguagesDescription[language.name]),
                callback_data = language.name,
            )
        )
    
    return markup


def handle_language_command(message : Message, bot : TeleBot):
    bot.send_message(
        message.chat.id,
        "Select language",
        reply_markup = get_language_markup(),
    )


def language_selection_cb(call, bot : TeleBot):

    _WhisperHelper().change_language(Languages[call.data])

    bot.send_message(
        call.from_user.id, 
        f"Language set to {LanguagesDescription[call.data]}"
    )
    bot.answer_callback_query(call.id, "")