from enum import Enum
import os
from functools import cache

from torch.cuda import is_available as is_cuda_available
from whisper_helper.model_names import ModelNames

class EnvKeys(Enum):

    BOT_TOKEN = "BOT_TOKEN"
    ADMIN_USER_ID = "ADMIN_USER_ID"
    MODEL_NAME = "MODEL_NAME"
    USE_FP16 = "MODEL_DTYPE"
    USE_CUDA = "USE_CUDA"
    DEVICE_ID = "DEVICE_ID"


@cache
def get_bot_token() -> str:
    """Retrieves the bot token from the environment variables.
    Since is a REQUIRED value, if not set, it will raise a KeyError if does not exist
    or ValueError if the default value has not been changed.

    Args:
    - bot_token_key : str - the key of the bot token environment variable

    Returns:
    - str - the bot token
    """
    try:
        bot_token = os.environ[EnvKeys.BOT_TOKEN.value]
    except ValueError:
        print(f"\"BOT_TOKEN\" has not been set.\n" +
                "Did you forget to set it?")
        raise ValueError
    except KeyError:
        print(f"\"BOT_TOKEN\" has not been found in the environment variables.\n" +
                "Did you forget to set it?")
        raise KeyError
        
    return bot_token

@cache
def get_admin_userid():
    """Retrieves the admin user id from the environment variables.
    Since is a REQUIRED value it will raise a KeyError if does not exist and a 
    ValueError if the value is not a number, i.e. is not changed from "YOUR_ADMIN_USER_ID"

    Args:
    - admin_userid_key : str - the key of the admin user id environment variable

    Returns:
    - int - the admin user id
    """
    
    try:
        admin_user_id = os.environ[EnvKeys.ADMIN_USER_ID.value]
        admin_user_id = int(admin_user_id)
    except ValueError:
        print(f"\"ADMIN_USER_ID\" is not a number.\n" +
                "Check bot_config.env!")
        raise ValueError
    except KeyError:
        print(f"\"ADMIN_USER_ID\" has not been found in the environment variables.\n" +
                "Did you forget to set it in bot_config.env?")
        raise KeyError
    
    return admin_user_id

@cache
def get_model_name():
    model_name = os.environ[EnvKeys.MODEL_NAME.value]

    if model_name in ModelNames.get_names():
        return ModelNames[model_name]
    else:
        return ModelNames.TINY

@cache
def get_use_cuda():    
    if not is_cuda_available():
        return False
    
    use_cuda = False

    try:
        use_cuda_env = os.environ[EnvKeys.USE_CUDA.value]
        use_cuda = bool(use_cuda_env)
    except KeyError:
        print(f"Environment variable in bot_config.env \"{EnvKeys.USE_CUDA.value}\" has not been found. Defaulting to False.")
    except ValueError:
        print(f"Environment variable in bot_config.env \"{EnvKeys.USE_CUDA.value}\" has True/False mispelled, defaulting to False.")
    
    return use_cuda


@cache
def get_use_fp16():
    if not get_use_cuda():
        return False
    
    use_fp16 = False

    try:
        use_fp16_env = os.environ[EnvKeys.USE_FP16.value]
        use_fp16 = bool(use_fp16_env)
    except KeyError:
        print(f"Environment variable in bot_config.env \"{EnvKeys.USE_FP16.value}\" has not been found. Defaulting to False.")
    except ValueError:
        print(f"Environment variable in bot_config.env \"{EnvKeys.USE_FP16.value}\" has True/False mispelled, defaulting to False.")
    
    return use_fp16


@cache
def get_device_id():
    if not get_use_cuda():
        return 0
    
    device_id = 0

    try:
        device_id_env = os.environ[EnvKeys.DEVICE_ID.value]
        device_id = int(device_id_env)
    except KeyError:
        print(f"Environment variable in bot_config.env \"{EnvKeys.DEVICE_ID.value}\" has not been found. Defaulting to 0.")
    except ValueError:
        print(f"Environment variable in bot_config.env \"{EnvKeys.DEVICE_ID.value}\" is not a number. Defaulting to 0.")
    
    return device_id