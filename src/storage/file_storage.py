from enum import Enum

from utils.result import Result
from .env_vars import env_vars
from .allowed_users_file import allowed_users_file

class StorageMessages(Enum):
    USER_ADD_IS_ADMIN = "%(user_id)s is ADMIN and cannot be added"
    USER_REMOVE_IS_ADMIN = "%(user_id)s is ADMIN and cannot be removed"

    def set_user(self, user_id):
        return self.value % {"user_id" : str(user_id)}


class _Storage():
    """Handles storage operations on both environment variables and files

    Makes public the following attributes:
    - bot_token : str - the bot token
    - admin_id : int - the admin id
    - allowed_users : list - the list of allowed users
    """
    def __init__(self):

        self.bot_token = env_vars.bot_token
        self.admin_id = env_vars.admin_id
        self.model_name = env_vars.model_name
        self.use_cuda = env_vars.use_cuda
        self.use_fp16 = env_vars.use_fp16
        self.device_id = env_vars.device_id

        self.allowed_users = allowed_users_file.allowed_users
    

    def add_user(self, user_id : int):
        """Adds a user to the allowed users list

        Args:
        - user_id : int - the user id to add

        Returns:
        - Result - the result of the operation with a message only if it failed
        """

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
        
    def purge_users(self):
        """Purges all users from the allowed users list

        Returns:
        - Result - the result of the operation, with a message only if it failed
        """

        result = allowed_users_file.purge_users()

        return Result(
            is_success = result.is_success,
            message = result.message
        )
    
    def remove_user(self, user_id : int):
        """Removes a user from the allowed users list

        Args:
        - user_id : int - the user id to remove

        Returns:
        - Result - the result of the operation, with a message only if it failed
        """
        
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