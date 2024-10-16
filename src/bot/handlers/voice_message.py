from enum import Enum
import os
import io

from telebot import TeleBot
from telebot.types import Message
from whisper_helper import whisper_model

CONTENT_TYPES = ["voice"]

# Received audio is temprarily saved in this folder, and removed when
# the transcription is done
TMP_FOLDER_PATH = "src/tmp"
FILE_NAME_TEMPLATE = "audio_%(message_id)s_%(message_date)s.ogg"


class Messages(Enum):
    VOICE_RECEIVED = "Audio message received, you will receive the transcription shortly... \n\n🗣️ → 🧠 → 📝"


def get_tmp_file_path(message_id, message_date):
    file_name = FILE_NAME_TEMPLATE % {"message_id" : str(message_id), "message_date" : str(message_date)}
    return f"{TMP_FOLDER_PATH}/{file_name}"

def handle_voice_message(message : Message, bot : TeleBot):
    
    bot.send_message(
        message.chat.id,
        Messages.VOICE_RECEIVED.value
    )

    file_info = bot.get_file(message.voice.file_id)
    file_path = file_info.file_path

    downloaded_file = bot.download_file(file_path)

    with io.BytesIO() as audio_buffer:
        audio_buffer.write(downloaded_file)
        audio_buffer.seek(0)
        result = whisper_model.to_text(audio_buffer.getbuffer())

    if result.is_success:
        bot.reply_to(message, result.data)
    else:
        bot.reply_to(message, result.message)