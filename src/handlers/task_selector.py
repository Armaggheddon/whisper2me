import telebot

from whisper_helper.tasks import Tasks, TasksDescription, TASK_KEY
from whisper_helper import _WhisperHelper


CMD = "task"
CB_LAMBDA = lambda call: call.data in Tasks.list_names()


def get_task_markup():
    markup = telebot.types.InlineKeyboardMarkup()
    markup.row_width = 2

    for task in Tasks:

        markup.add(
            telebot.types.InlineKeyboardButton(
                str(TasksDescription[task.name]),
                callback_data = task.name
            )
        )
    
    return markup


def handle_task_command(message, bot):
    bot.send_message(
        message.chat.id,
        "Select task",
        reply_markup = get_task_markup()
    )


def task_selection_cb(call, bot):

    _WhisperHelper().change_language(Tasks[call.data])

    bot.send_message(
        call.from_user.id, 
        f"Task set to {TasksDescription[call.data]}"
    )
    bot.answer_callback_query(call.id, "")