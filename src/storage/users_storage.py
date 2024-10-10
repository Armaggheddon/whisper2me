import sqlite3
from enum import Enum

from .env_vars import get_admin_userid
from utils.result import Result


class StorageMessages(Enum):
    USER_ADD_ALREADY_IN = "%(user_id)s is already allowed"
    USER_ALREADY_REMOVED = "%(user_id)s is already not allowed"
    USER_PURGE_LIST_ALREADY_EMPY = "The list is already empty"
    USER_ADD_IS_ADMIN = "%(user_id)s is ADMIN and cannot be added"
    USER_REMOVE_IS_ADMIN = "%(user_id)s is ADMIN and cannot be removed"

    def set_user(self, user_id):
        """Sets the user id in the message
        
        Args:
        - user_id - the user id to set
        """
        return self.value % {"user_id" : str(user_id)}


_db_path = "/whisper2me_bot_data/allowed_users.db"


class UsersStorage:

    _instance = None

    @staticmethod
    def get_instance():
        if UsersStorage._instance == None:
            UsersStorage._instance = UsersStorage(get_admin_userid())
        return UsersStorage._instance
    
    def __init__(self, admin_user_id: str):
        self.admin_user_id = admin_user_id
        
        self._conn = sqlite3.connect(_db_path)
        self._cursor = self._conn.cursor()

        self._cursor.execute("""
            CREATE TABLE IF NOT EXISTS allowed_users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                telegram_user_id INTEGER NOT NULL UNIQUE
            )
        """)

        self._conn.commit()
        self._conn.close()
    

    def _with_db(func):
        def wrapper(self, *args, **kwargs):
            self._conn = sqlite3.connect(_db_path, check_same_thread=False)
            self._cursor = self._conn.cursor()
            result = func(self, *args, **kwargs)
            self._conn.close()
            return result
        return wrapper

    @_with_db
    def add_user(self, user_id: int):

        if user_id == self.admin_user_id:
            return Result(
                is_success=False,
                message=StorageMessages.USER_ADD_IS_ADMIN.set_user(user_id)
            )

        try:
            self._cursor.execute("INSERT INTO allowed_users (telegram_user_id) VALUES (?)", (user_id,))
            self._conn.commit()
        except sqlite3.IntegrityError:
            return Result(
                is_success=False,
                message=StorageMessages.USER_ADD_ALREADY_IN.set_user(user_id)
            )

        return Result(is_success=True)
    
    @_with_db
    def list_users(self):
        self._cursor.execute("SELECT telegram_user_id FROM allowed_users")
        return [row[0] for row in self._cursor.fetchall()]
    
    @_with_db
    def remove_user(self, user_id: int):
        self._cursor.execute("DELETE FROM allowed_users WHERE telegram_user_id = ?", (user_id,))
        self._conn.commit()

        if self._cursor.rowcount == 0:
            return Result(
                is_success=False,
                message=StorageMessages.USER_ALREADY_REMOVED.set_user(user_id)
            )
        
        return Result(is_success=True)
        
    @_with_db
    def purge_users(self):
        self._cursor.execute("DELETE FROM allowed_users")
        self._conn.commit()

        if self._cursor.rowcount == 0:
            return Result(
                is_success=False,
                message=StorageMessages.USER_PURGE_LIST_ALREADY_EMPY.value
            )
        
        
        return Result(is_success=True)

