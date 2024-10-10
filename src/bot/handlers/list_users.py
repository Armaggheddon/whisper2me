from enum import Enum
from telebot import TeleBot
from telebot.types import Message

from storage import UsersStorage, env_vars
from utils.user_formats import UserFormats

CMD = "users"


class Messages(Enum):
    HEADER = "Currently allowed users are:\n\n"


def get_users_printable():

    users_str = ""

    users_str += UserFormats.USER_ADMIN.set_user(env_vars.get_admin_userid()) + "\n"

    for user in UsersStorage.get_instance().list_users():
        users_str += "\n"
        users_str += UserFormats.USER_NORMAL.set_user(user)
    
    return users_str


def handle_list_users(message, bot):

    message_header = Messages.HEADER.value

    response = message_header + get_users_printable()

    bot.send_message(
        message.chat.id,
        response
    )