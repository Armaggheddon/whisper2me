from telebot import TeleBot
from telebot.types import Message

from storage import storage

def handle_non_admin_endpoint(message, bot):

    bot.send_message(
        message.chat.id,
        f"You are not the ADMIN..., bad luck :(\n\nThe ADMIN has been informed 🥲"
    )

    bot.send_message(
        storage.admin_id,
        f"⚠️ {message.chat.id} tried an ADMIN command ⚠️\n\n{message.text}"
    )