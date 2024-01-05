from enum import Enum
from utils.result import Result


class StorageFileNames(Enum):
    FILE_NAME =     "persistent_data/allowed_users.txt"
    BAK_FILE_NAME = "persistent_data/allowed_users.bak"

class Messages(Enum):
    USER_ADD_ALREADY_IN =       "%(user_id)s is already allowed"
    USER_REMOVE_ALREADY_IN =    "%(user_id)s is already not allowed"
    USER_PURGE_LIST_ALREADY_EMPY = "The list is already empty"

    def set_user(self, user_id):
        """Sets the user id in the message
        
        Args:
        - user_id - the user id to set
        """
        return self.value % {"user_id" : str(user_id)}
    

class _AllowedUsersFile():
    """Helper class to manage the allowed users file
    """
    
    def __init__(self):
        
        self.allowed_users = self.get_allowed_users()


    def get_allowed_users(self):
        _tmp = []

        with open(StorageFileNames.FILE_NAME.value, "r") as f:
            lines = f.readlines()

            for line in lines:

                _tmp.append(int(line.strip()))

        return _tmp


    def perform_with_update(self, func, user_id = None):
        """Performs the given function and updates the file as long as the backup file
        
        Args:
        - func - the function to perform
        - user_id - the user id to pass to the function
        """
        self.update_file(StorageFileNames.BAK_FILE_NAME)

        if user_id != None:
            func(user_id)
        else:
            func()

        self.update_file(StorageFileNames.FILE_NAME)

    
    def update_file(self, file_name : StorageFileNames):
        """Updates the list of allowed users in the file with the given file name

        Args:
        - file_name : StorageFileNames - the file name to update
        """
        with open(file_name.value, "w") as f:

            formatted_str = ""
            for i, user_id in enumerate(self.allowed_users):
                formatted_str += str(user_id)

                if i != len(self.allowed_users) - 1:
                    formatted_str += "\n"
            
            f.write(formatted_str)


    def add_user(self, user_id : int):
        """Adds a user to the allowed users list

        Args:
        - user_id : int - the user id to add

        Returns:
        - Result - the result of the operation with a message only if it failed
        """
        result = Result(is_success = False)

        if user_id not in self.allowed_users:
            self.perform_with_update(self.allowed_users.append, user_id)
            result.is_success = True
        else:
            result.message = Messages.USER_ADD_ALREADY_IN.set_user(user_id)
        return result
    

    def purge_users(self):
        """Purges all users from the allowed users list
        
        Returns:
        - Result - the result of the operation, with a message only if it failed
        """
        if len(self.allowed_users) == 0:
            return Result(
                is_success = False,
                message = Messages.USER_PURGE_LIST_ALREADY_EMPY.value
            )
        
        result = Result(is_success=False)

        self.perform_with_update(self.allowed_users.clear)
        result.is_success = True

        return result

    def remove_user(self, user_id : int):
        """Removes a user from the allowed users list
        
        Args:
        - user_id : int - the user id to remove
        
        Returns:
        - Result - the result of the operation, with a message only if it failed
        """
        result = Result(is_success=False)

        if user_id in self.allowed_users:
            self.perform_with_update(self.allowed_users.remove, user_id)
            result.is_success = True
        else:
            result.message = Messages.USER_REMOVE_ALREADY_IN.set_user(user_id)

        return result


allowed_users_file = _AllowedUsersFile()