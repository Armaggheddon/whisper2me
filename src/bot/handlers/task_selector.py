from enum import Enum

from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from whisper_helper.tasks import Tasks, TasksDescription, TASK_KEY
from whisper_helper import whisper_model


CMD = "task"

SELECT_TASK_CB_PREFIX = "T "
CB_LAMBDA = lambda call: call.data[:len(SELECT_TASK_CB_PREFIX)] == SELECT_TASK_CB_PREFIX
DATA_FROM_CB = lambda call : call.data[len(SELECT_TASK_CB_PREFIX):]

class Messages(Enum):
    COMMAND_HEAD = "Select task:"
    BUTTON_CANCEL = "❌ Cancel"
    BUTTON_CANCEL_CB_DATA = "CANCEL"
    
    TASK_SET_TO = "Task set to %(task)s"

    def with_task(self, task):
        if self != Messages.TASK_SET_TO:
            return self.value
        
        return self.value % {"task" : str(task)}

def build_cb_data(data):
    return f"{SELECT_TASK_CB_PREFIX}{data}"

def get_task_markup():
    markup = InlineKeyboardMarkup(row_width=2)

    buttons = [
        InlineKeyboardButton(
            str(TasksDescription[task.name]),
            callback_data = build_cb_data(task.name)
        ) for task in Tasks
    ]
    markup.add(*buttons)

    
    markup.add(
        InlineKeyboardButton(
            Messages.BUTTON_CANCEL.value, 
            callback_data = build_cb_data(Messages.BUTTON_CANCEL_CB_DATA.value)
        )
    )
    
    return markup


def handle_task_command(message, bot):
    bot.send_message(
        message.chat.id,
        Messages.COMMAND_HEAD.value,
        reply_markup = get_task_markup()
    )


def task_selection_cb(call, bot):

    data = DATA_FROM_CB(call)

    if data == Messages.BUTTON_CANCEL_CB_DATA.value:
        bot.send_message(
            call.from_user.id, 
            Messages.BUTTON_CANCEL.value
        )
    else:
        whisper_model.change_task(Tasks[data])

        bot.send_message(
            call.from_user.id, 
            Messages.TASK_SET_TO.with_task(TasksDescription[data])
        )

    # Remove markup for buttons and delete language selection message
    # Remains only the response of the selection
    bot.edit_message_reply_markup(
        chat_id = call.message.chat.id,
        message_id = call.message.id,
        reply_markup="")
    bot.delete_message(
        chat_id = call.message.chat.id,
        message_id = call.message.id
    )
        
    bot.answer_callback_query(call.id, "")