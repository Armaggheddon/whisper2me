import sqlite3
from enum import Enum
from typing import Union

class SettingKeys(Enum):
    MODEL_LANGUAGE = "model_language"
    MODEL_TASK = "model_task"


_db_path = "/whisper2me_bot_data/bot_settings.db"


class BotSettings:
    _instance = None

    @staticmethod
    def get_instance():
        if BotSettings._instance == None:
            BotSettings._instance = BotSettings()
        return BotSettings._instance
    
    
    def __init__(self):

        self._conn = sqlite3.connect(_db_path)
        self._cursor = self._conn.cursor()

        self._cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS bot_settings (
                setting_name TEXT PRIMARY KEY,
                setting_value TEXT
            )
            """
        )

        self._conn.commit()
        self._conn.close()

        self._initialize()

 
    def _with_db(func):
        def wrapper(self, *args, **kwargs):
            self._conn = sqlite3.connect(_db_path, check_same_thread=False)
            self._cursor = self._conn.cursor()
            result = func(self, *args, **kwargs)
            self._conn.close()
            return result
        return wrapper
    

    def _is_table_empty(self):
        self._cursor.execute("SELECT COUNT(*) FROM bot_settings")
        return self._cursor.fetchone()[0] == 0


    @_with_db
    def _initialize(self):

        default_settings = {
            SettingKeys.MODEL_LANGUAGE.value: "it",
            SettingKeys.MODEL_TASK.value: "transcribe"
        }

        if self._is_table_empty():
            for key, value in default_settings.items():
                self._cursor.execute(
                    "INSERT INTO bot_settings (setting_name, setting_value) VALUES (?, ?)",
                    (key, value)
                )
            self._conn.commit()


    @_with_db
    def get_setting(self, key: SettingKeys):
        self._cursor.execute(
            "SELECT setting_value FROM bot_settings WHERE setting_name = ?",
            (key.value,)
        )
        return self._cursor.fetchone()[0]


    @_with_db
    def set_setting(self, key: SettingKeys, value: str):
        self._cursor.execute(
            "UPDATE bot_settings SET setting_value = ? WHERE setting_name = ?",
            (value, key.value)
        )
        self._conn.commit()
        return value

