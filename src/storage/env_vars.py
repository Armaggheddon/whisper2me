from enum import Enum
import os
from whisper_helper.model_names import ModelNames

class EnvKeys(Enum):

    BOT_TOKEN = "BOT_TOKEN"
    ADMIN_USER_ID = "ADMIN_USER_ID"
    # MODEL_NAME = "MODEL_NAME"


class _EnvVars():
    
    def __init__(
            self,
            bot_token_key : str = EnvKeys.BOT_TOKEN.value,
            admin_userid_key : str = EnvKeys.ADMIN_USER_ID.value,
            # model_name_key : str = EnvKeys.MODEL_NAME.value
    ):
        
        self.bot_token = self.get_bot_token(bot_token_key)
        self.admin_id = self.get_admin_userid(admin_userid_key)
        # self.model_name = self.get_model_name(model_name_key)
    

    def get_bot_token(self, bot_token_key : str) -> str:
        return os.environ[bot_token_key]
    
    def get_admin_userid(self, admin_userid_key):
        
        admin_user_id = os.environ[admin_userid_key]

        try:
            admin_user_id = int(admin_user_id)
        except ValueError:
            admin_user_id = None
        
        return admin_user_id

    # def get_model_name(model_name_key):
    #     model_name = os.environ[model_name_key]

    #     if model_name in ModelNames.get_names():
    #         return ModelNames[model_name]
    #     else:
    #         return ModelNames.TINY
    
env_vars = _EnvVars()