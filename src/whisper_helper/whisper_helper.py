"""
This module contains the WhisperHelper class, which is used to perform
operations with the whisper model. It also contains the default whisper helper
initialized with the values retrieved from storage. 

Use whisper_helper to:
- change the task performed by the whisper model
- change the language used by the whisper model
- transcribe/translate an audio message, using the current settings
"""
import whisper

from .languages import Languages, LANGUAGE_KEY
from .model_names import ModelNames, MODEL_NAME_KEY
from .tasks import Tasks, TASK_KEY
from .devices import Devices, DEVICE_KEY
from .model_dtypes import ModelDtypes, DTYPE_KEY
from .audio import load_audio_from_bytes
from utils.result_with_data import ResultWithData
from storage import env_vars, BotSettings, SettingKeys


_model_cache_root = "/whisper2me_bot_data/model_cache"
  

class _WhisperHelper():
    """Helper class for whisper operations
    """
    
    _settings = {
        LANGUAGE_KEY: Languages.ITALIAN,
        TASK_KEY: Tasks.TRANSCRIBE,
        MODEL_NAME_KEY: ModelNames.TINY,
        DTYPE_KEY: ModelDtypes.FP32,
        DEVICE_KEY: Devices.CPU,
        "device_id": 0
    }

    def __init__(
            self,
            model_name = ModelNames.TINY,
            use_fp16 = ModelDtypes.FP32,
            device = Devices.CPU,
            device_id = 0
    ):
        """Initializes the whisper model
        
        Args:
        - language : Languages - the language to use
        - task : Tasks - the task to perform
        - model_name : ModelNames - the model name to use
        - use_fp16 : ModelDtypes - whether to use fp16 or not, CPU supports only fp32
        - device : Devices - the device to use, supported devices are CPU and CUDA
        - device_id : int - the id of the device to use, ignored if device is CPU or if only one GPU is available
        """

        _WhisperHelper._settings[LANGUAGE_KEY] = Languages(
            BotSettings.get_instance().get_setting(
                SettingKeys.MODEL_LANGUAGE))

        _WhisperHelper._settings[TASK_KEY] = Tasks(
            BotSettings.get_instance().get_setting(
                SettingKeys.MODEL_TASK))
        
        _WhisperHelper._settings[MODEL_NAME_KEY] = model_name
            
        _WhisperHelper._settings[DEVICE_KEY] = device
        if device == Devices.CPU.value:
            _WhisperHelper._settings[DTYPE_KEY] = ModelDtypes.FP32
        else:
            _WhisperHelper._settings[DTYPE_KEY] = use_fp16
        
        _WhisperHelper._settings["device_id"] = device_id

        self.model = whisper.load_model(
            _WhisperHelper._settings[MODEL_NAME_KEY].value,
            download_root = _model_cache_root
        )
        if _WhisperHelper._settings[DEVICE_KEY] != Devices.CPU:
            self.model.to(
                _WhisperHelper._settings[DEVICE_KEY].with_id(
                    _WhisperHelper._settings["device_id"]
                )
            )

    def get_settings(self):
        """Returns the current settings used by the whisper model
        
        Returns:
        - dict - the current settings
        """
        return _WhisperHelper._settings

    def change_task(self, task):
        """Changes the task performed by the whisper model

        Args:
        - task : Tasks - the task to perform
        """
        _WhisperHelper._settings[TASK_KEY] = Tasks(
            BotSettings.get_instance().set_setting(
                SettingKeys.MODEL_TASK,
                task.value
            )
        )


    def change_language(self, language):
        """Changes the language used by the whisper model
        
        Args:
        - language : Languages - the language to use
        """
        _WhisperHelper._settings[LANGUAGE_KEY] = Languages(
            BotSettings.get_instance().set_setting(
                SettingKeys.MODEL_LANGUAGE,
                language.value
            )
        )


    def to_text(self, audio_byte_buffer):
        """Transcribes/translates the audio message at the given path
        
        Args:
        - audio_path : str - the path to the audio message

        Returns:
        - ResultWithData - the result of the operation, with 
        the transcribed/translated text if successful, or a message if not
        """

        model_result = self.model.transcribe(
            load_audio_from_bytes(audio_byte_buffer),
            language = _WhisperHelper._settings[LANGUAGE_KEY].value,
            task = _WhisperHelper._settings[TASK_KEY].value,
            fp16 = _WhisperHelper._settings[DTYPE_KEY].value,
        )

        result = ResultWithData()
        try:
            audio_text = model_result["text"]

            result.is_success = True
            result.data = audio_text

        except KeyError:
            result.message = "An error occurred while processing the audio message. Try again"
        
        return result
    

# Default whisper helper
whisper_model = _WhisperHelper(
    model_name=env_vars.get_model_name(),
    device=Devices.CUDA if env_vars.get_use_cuda() else Devices.CPU,
    use_fp16=ModelDtypes.FP16 if env_vars.get_use_fp16() else ModelDtypes.FP32,
    device_id=env_vars.get_device_id()
)