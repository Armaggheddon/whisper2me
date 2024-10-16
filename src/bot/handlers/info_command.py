from enum import Enum
from telebot import TeleBot
from telebot.types import Message

from whisper_helper.model_names import MODEL_NAME_KEY
from whisper_helper.languages import LANGUAGE_KEY, LanguagesDescription
from whisper_helper.model_dtypes import DTYPE_KEY
from whisper_helper.devices import Devices, DEVICE_KEY
from whisper_helper.tasks import TASK_KEY, TasksDescription
from whisper_helper import whisper_model

CMD = "info"

class Messages(Enum):
    COMMAND_HEAD = "ℹ️ Bot information:\n\n"
    MODEL_NAME = "- Using model %(model_name)s\n"
    TASK_LANGUAGE = "- %(model_task)s to %(model_language)s\n"
    IS_CUDA_DTYPE = "- Using CUDA with %(model_dtype)s%(GPU_ID)s\n"
    IS_CPU = "- Using CPU with FP32\n"

    def with_model_name(self, model_name):
        if self != Messages.MODEL_NAME:
            return self.value
        return self.value % {"model_name" : str(model_name)}
    
    def with_task_language(self, task, language):
        if self != Messages.TASK_LANGUAGE:
            return self.value
        return self.value % {"model_task" : str(task), "model_language" : str(language)}
    
    def with_model_dtype(self, model_dtype, gpu_id = 0):
        if self != Messages.IS_CUDA_DTYPE:
            return self.value
        return self.value % {"model_dtype" : str(model_dtype), "GPU_ID" : f" on GPU:{gpu_id}"}

def model_dtype_to_string(model_dtype):
    # model_dtype is a boolean, True for FP16, False for FP32
    return f"{'FP16' if model_dtype else 'FP32'}"  

def handle_info_command(message : Message, bot : TeleBot):

    result = Messages.COMMAND_HEAD.value

    whisper_settings = whisper_model.get_settings()

    result += Messages.MODEL_NAME.with_model_name(whisper_settings[MODEL_NAME_KEY].value)
    print(whisper_settings[TASK_KEY])
    task_printable = TasksDescription[whisper_settings[TASK_KEY].name]
    language_printable = LanguagesDescription[whisper_settings[LANGUAGE_KEY].name]
    
    result += Messages.TASK_LANGUAGE.with_task_language(task_printable, language_printable)
    
    device = whisper_settings[DEVICE_KEY]
    if device == Devices.CPU:
        result += Messages.IS_CPU.value
    else:
        result += Messages.IS_CUDA_DTYPE.with_model_dtype(
            model_dtype_to_string(whisper_settings[DTYPE_KEY].value), 
            whisper_settings["device_id"]
        )
    
    bot.send_message(
        message.chat.id,
        result
    )

    