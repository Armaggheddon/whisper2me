from enum import Enum

from utils.result import Result
from storage.env_vars import env_vars
from storage.allowed_users_file import allowed_users_file

class StorageMessages(Enum):
    USER_ADD_IS_ADMIN = "%(user_id)s is ADMIN and cannot be added"
    USER_REMOVE_IS_ADMIN = "%(user_id)s is ADMIN and cannot be removed"

    def set_user(self, user_id):
        return self.value % {"user_id" : str(user_id)}


class _Storage():

    def __init__(self):

        self.bot_token = env_vars.bot_token
        self.admin_id = env_vars.admin_id
        # self.model_name = env_vars.model_name

        self.allowed_users = allowed_users_file.allowed_users
    

    def add_user(self, user_id : int):

        if user_id == self.admin_id:
            return Result(
                is_success=False,
                message=StorageMessages.USER_ADD_IS_ADMIN.set_user(user_id)
            )
        
        result = allowed_users_file.add_user(user_id)
        if result.is_success:
            self.allowed_users = allowed_users_file.allowed_users
            return Result(is_success=True)
        else:
            return Result(
                is_success=False,
                message = result.message
            )
    
    def remove_user(self, user_id : int):

        if user_id == self.admin_id:
            return Result(
                is_success=False,
                message = StorageMessages.USER_REMOVE_IS_ADMIN.set_user(user_id)
            )
        
        result = allowed_users_file.remove_user(user_id)
        if result.is_success:
            self.allowed_users = allowed_users_file.allowed_users
            return Result(is_success = True)
        else:
            return Result(
                is_success = False,
                message = result.message
            )

storage = _Storage()