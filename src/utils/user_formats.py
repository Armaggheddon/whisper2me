from enum import Enum

class UserFormats(Enum):
    USER_ADMIN =            "🧞 %(user_id)s (You)\n"
    USER_NORMAL =           "👤 %(user_id)s"

    def set_user(self, user_id):
        return self.value % {"user_id" : str(user_id)}