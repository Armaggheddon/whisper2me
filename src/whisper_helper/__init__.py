import whisper
from enum import Enum
from .languages import Languages, LANGUAGE_KEY
from .model_names import ModelNames, MODEL_NAME_KEY
from .tasks import Tasks, TASK_KEY
from .devices import Devices, DEVICE_KEY
from .model_dtypes import ModelDtypes, DTYPE_KEY
from utils.result_with_data import ResultWithData


class WhisperSettings():
    settings = {
        LANGUAGE_KEY :      Languages.ITALIAN,
        TASK_KEY :          Tasks.TRANSCRIBE,
        MODEL_NAME_KEY :    ModelNames.TINY,
        DTYPE_KEY :         ModelDtypes.FP32,
        DEVICE_KEY :        Devices.CPU,
        "device_id" :       0
    }

class _WhisperHelper():
    
    def __init__(
            self,
            language = Languages.ITALIAN,
            task = Tasks.TRANSCRIBE,
            model_name = ModelNames.TINY,
            use_fp16 = ModelDtypes.FP32,
            device = Devices.CPU,
            device_id = 0
    ):
        
        WhisperSettings.settings[LANGUAGE_KEY] = language
        WhisperSettings.settings[TASK_KEY] = task
        WhisperSettings.settings[MODEL_NAME_KEY] = model_name
            
        WhisperSettings.settings[DEVICE_KEY] = device
        if device == Devices.CPU.value:
            WhisperSettings.settings[DTYPE_KEY] = ModelDtypes.FP32
        else:
            WhisperSettings.settings[DTYPE_KEY] = use_fp16
        
        WhisperSettings.settings["device_id"] = device_id

        self.model = whisper.load_model(
            WhisperSettings.settings[MODEL_NAME_KEY].value
        )
        if WhisperSettings.settings[DEVICE_KEY] != Devices.CPU:
            self.model.to(
                WhisperSettings.settings[DEVICE_KEY].with_id(
                    WhisperSettings.settings["device_id"]
                )
            )

    def change_task(self, task):
        WhisperSettings.settings[TASK_KEY] = task

    def change_language(self, language):
        WhisperSettings.settings[LANGUAGE_KEY] = language
    

    def to_text(self, audio_path):

        model_result = self.model.transcribe(
            audio_path,
            language = WhisperSettings.settings[LANGUAGE_KEY].value,
            task = WhisperSettings.settings[TASK_KEY].value,
            fp16 = WhisperSettings.settings[DTYPE_KEY].value,
        )

        result = ResultWithData()
        try:
            audio_text = model_result["text"]

            result.is_success = True
            result.data = audio_text

        except KeyError:
            result.message = "An error occurred while processing the audio message. Try again"
        
        return result
    

whisper_helper = _WhisperHelper(
    model_name = ModelNames.TINY,
    device = Devices.CPU,
    use_fp16=ModelDtypes.FP32,
    device_id=0
)

def change_backend_settings(
    model_name : ModelNames = ModelNames.TINY,
    use_fp16 : ModelDtypes = ModelDtypes.FP32, 
    device : Devices = Devices.CPU,
    device_id : int = 0,
):
    global whisper_helper
    whisper_helper = _WhisperHelper(
        model_name=model_name,
        use_fp16=use_fp16,
        device=device,
        device_id=device_id
    )
