from torch.cuda import is_available as is_cuda_available

from enum import Enum
import os
from whisper_helper.model_names import ModelNames

class EnvKeys(Enum):

    BOT_TOKEN = "BOT_TOKEN"
    ADMIN_USER_ID = "ADMIN_USER_ID"
    MODEL_NAME = "MODEL_NAME"
    USE_FP16 = "MODEL_DTYPE"
    USE_CUDA = "CUDA"
    DEVICE_ID = "DEVICE_ID"


class _EnvVars():
    '''Helper class to retrieve environment variables
    '''


    def __init__(
            self,
            bot_token_key : str = EnvKeys.BOT_TOKEN.value,
            admin_userid_key : str = EnvKeys.ADMIN_USER_ID.value,
            model_name_key : str = EnvKeys.MODEL_NAME.value,
            use_cuda_key : str = EnvKeys.USE_CUDA.value,
            use_fp16_key : str = EnvKeys.USE_FP16.value,
            device_id_key : str = EnvKeys.DEVICE_ID.value,
    ):
        '''
        Args:
        - bot_token_key : str - the key of the bot token environment variable
        - admin_userid_key : str - the key of the admin user id environment variable
        '''
        self.bot_token = self.get_bot_token(bot_token_key)
        self.admin_id = self.get_admin_userid(admin_userid_key)
        self.model_name = self.get_model_name(model_name_key)
        self.use_cuda = self.get_use_cuda(use_cuda_key) if is_cuda_available() else False
        self.use_fp16 = self.get_use_fp16(use_fp16_key) if self.use_cuda else False
        self.device_id = 0 if not self.use_cuda else self.get_device_id(device_id_key)
    

    def get_bot_token(self, bot_token_key : str) -> str:
        # TODO: Comment method REQUIRED VALUE!!, KeyError if not set
        try:
            bot_token = os.environ[bot_token_key]
            if bot_token == "YOUR_BOT_TOKEN": raise ValueError
            return bot_token
        except ValueError:
            print(f"\"BOT_TOKEN\" has not been set in the Dockerfile.\n" +
                  "Did you forget to set it?")
            raise ValueError
        except KeyError:
            print(f"\"BOT_TOKEN\" has not been found in the environment variables.\n" +
                  "Did you forget to set it?")
            raise KeyError
    
    def get_admin_userid(self, admin_userid_key):
        # TODO: Comment method REQUIRED VALUE!!, KeyError if not set, ValueError if is not a number
        
        try:
            admin_user_id = os.environ[admin_userid_key]
            admin_user_id = int(admin_user_id)
        except ValueError:
            print(f"\"ADMIN_USER_ID\" is not a number.\n" +
                  "Check the Dockerfile!")
            raise ValueError
        except KeyError:
            print(f"\"ADMIN_USER_ID\" has not been found in the environment variables.\n" +
                  "Did you forget to set it in the Dockerfile?")
            raise KeyError
        
        return admin_user_id

    def get_model_name(self, model_name_key):
        model_name = os.environ[model_name_key]

        if model_name in ModelNames.get_names():
            return ModelNames[model_name]
        else:
            return ModelNames.TINY
    
    def get_use_cuda(self, use_cuda_key:str):
        
        use_cuda = False

        try:
            use_cuda_env = os.environ[use_cuda_key]
            use_cuda = bool(use_cuda_env)
        except KeyError:
            print(f"Environment variable in Dockerfile \"{EnvKeys.USE_CUDA.value}\" has not been found. Defaulting to False.")
        except ValueError:
            print(f"Environment variable in Dockerfile \"{EnvKeys.USE_CUDA.value}\" has True/False mispelled, defaulting to False.")
        
        return use_cuda
    
    def get_use_fp16(self, use_fp16_key:str):
        use_fp16 = False

        try:
            use_fp16_env = os.environ[use_fp16_key]
            use_fp16 = bool(use_fp16_env)
        except KeyError:
            print(f"Environment variable in Dockerfile \"{EnvKeys.USE_FP16.value}\" has not been found. Defaulting to False.")
        except ValueError:
            print(f"Environment variable in Dockerfile \"{EnvKeys.USE_FP16.value}\" has True/False mispelled, defaulting to False.")
        
        return use_fp16

    def get_device_id(self, device_id_key:str):

        device_id = 0

        try:
            device_id_env = os.environ[device_id_key]
            device_id = int(device_id_env)
        except KeyError:
            print(f"Environment variable in Dockerfile \"{EnvKeys.DEVICE_ID.value}\" has not been found. Defaulting to 0.")
        except ValueError:
            print(f"Environment variable in Dockerfile \"{EnvKeys.DEVICE_ID.value}\" is not a number. Defaulting to 0.")
        
        return device_id

    
env_vars = _EnvVars()