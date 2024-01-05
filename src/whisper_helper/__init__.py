import whisper
from .languages import Languages, LANGUAGE_KEY
from .model_names import ModelNames, MODEL_NAME_KEY
from .tasks import Tasks, TASK_KEY
from .devices import Devices, DEVICE_KEY
from .model_dtypes import ModelDtypes, DTYPE_KEY
from utils.result_with_data import ResultWithData
from storage import storage

MODEL_CACHE_ROOT = "persistent_data/model_cache"

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
    '''Helper class for whisper operations
    '''
    
    def __init__(
            self,
            language = Languages.ITALIAN,
            task = Tasks.TRANSCRIBE,
            model_name = ModelNames.TINY,
            use_fp16 = ModelDtypes.FP32,
            device = Devices.CPU,
            device_id = 0
    ):
        '''Initializes the whisper model
        
        Args:
        - language : Languages - the language to use
        - task : Tasks - the task to perform
        - model_name : ModelNames - the model name to use
        - use_fp16 : ModelDtypes - whether to use fp16 or not, CPU supports only fp32
        - device : Devices - the device to use, supported devices are CPU and CUDA
        - device_id : int - the id of the device to use, ignored if device is CPU or if only one GPU is available
        '''
        WhisperSettings.settings[LANGUAGE_KEY] = language
        WhisperSettings.settings[TASK_KEY] = task
        WhisperSettings.settings[MODEL_NAME_KEY] = model_name
        #TODO: check if model cache already exists, so that it can be used instead
        # of having to redownload the model every time
            
        WhisperSettings.settings[DEVICE_KEY] = device
        if device == Devices.CPU.value:
            WhisperSettings.settings[DTYPE_KEY] = ModelDtypes.FP32
        else:
            WhisperSettings.settings[DTYPE_KEY] = use_fp16
        
        WhisperSettings.settings["device_id"] = device_id

        self.model = whisper.load_model(
            WhisperSettings.settings[MODEL_NAME_KEY].value,
            download_root = "persistent_data/model_cache"
        )
        if WhisperSettings.settings[DEVICE_KEY] != Devices.CPU:
            self.model.to(
                WhisperSettings.settings[DEVICE_KEY].with_id(
                    WhisperSettings.settings["device_id"]
                )
            )

    def change_task(self, task):
        '''Changes the task performed by the whisper model

        Args:
        - task : Tasks - the task to perform
        '''
        WhisperSettings.settings[TASK_KEY] = task


    def change_language(self, language):
        '''Changes the language used by the whisper model
        
        Args:
        - language : Languages - the language to use
        '''
        WhisperSettings.settings[LANGUAGE_KEY] = language
    

    def to_text(self, audio_path):
        '''Transcribes/translates the audio message at the given path
        
        Args:
        - audio_path : str - the path to the audio message

        Returns:
        - ResultWithData - the result of the operation, with 
        the transcribed/translated text if successful, or a message if not
        '''

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
    

# Default whisper helper
from storage import storage
whisper_helper = _WhisperHelper(
    model_name=storage.model_name,
    device=Devices.CUDA if storage.use_cuda else Devices.CPU,
    use_fp16=ModelDtypes.FP16 if storage.use_fp16 else ModelDtypes.FP32,
    device_id=storage.device_id
)