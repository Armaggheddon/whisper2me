from enum import Enum
from utils.result import Result


class StorageFileNames(Enum):
    FILE_NAME =     "allowed_users.txt"
    BAK_FILE_NAME = "allowed_users.bak"

class Messages(Enum):
    USER_ADD_ALREADY_IN =       "%(user_id)s is already allowed"
    USER_REMOVE_ALREADY_IN =    "%(user_id)s is already not allowed"

    def set_user(self, user_id):
        return self.value % {"user_id" : str(user_id)}
    

class _AllowedUsersFile():
    
    def __init__(self):
        
        self.allowed_users = self.get_allowed_users()


    def get_allowed_users(self):
        _tmp = []

        with open(StorageFileNames.FILE_NAME.value, "r") as f:
            lines = f.readlines()

            for line in lines:

                _tmp.append(int(line.strip()))

        return _tmp


    def perform_with_update(self, func, user_id):
        self.update_file(StorageFileNames.BAK_FILE_NAME)

        func(user_id)

        self.update_file(StorageFileNames.FILE_NAME)

    
    def update_file(self, file_name : StorageFileNames):
        with open(file_name.value, "w") as f:

            formatted_str = ""
            for i, user_id in enumerate(self.allowed_users):
                formatted_str += str(user_id)

                if i != len(self.allowed_users) - 1:
                    formatted_str += "\n"
            
            f.write(formatted_str)


    def add_user(self, user_id : int):
        # TODO: caller must ensure user_id IS NOT ADMIN
        result = Result(is_success = False)

        if user_id not in self.allowed_users:
            self.perform_with_update(self.allowed_users.append, user_id)
            result.is_success = True
        else:
            result.message = Messages.USER_ADD_ALREADY_IN.set_user(user_id)
        return result

    def remove_user(self, user_id : int):
        # TODO: caller must ensure user_id IS NOT ADMIN
        result = Result(is_success=False)

        if user_id in self.allowed_users:
            self.perform_with_update(self.allowed_users.remove, user_id)
            result.is_success = True
        else:
            result.message = Messages.USER_REMOVE_ALREADY_IN.set_user(user_id)

        return result


allowed_users_file = _AllowedUsersFile()