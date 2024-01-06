from enum import Enum

LANGUAGE_KEY = "language"

class Languages(Enum):

    ENGLISH = "en"
    FRENCH = "fr"
    GERMAN = "de"
    ITALIAN = "it"
    SPANISH = "es"

    @classmethod
    def list_names(cls):
        return [i.name for i in Languages]
    
    @classmethod
    def list_values(cls):
        return [i.value for i in Languages]


class LanguagesDescription(Enum):

    ENGLISH = {
        "full_name" : "english",
        "flag_emoji" : "🇺🇸"
    }

    ITALIAN = {
        "full_name" : "italian",
        "flag_emoji" : "🇮🇹"
    }

    SPANISH = {
        "full_name" : "spanish",
        "flag_emoji" : "🇪🇸"
    }

    GERMAN = {
        "full_name" : "german",
        "flag_emoji" : "🇩🇪"
    }

    FRENCH = {
        "full_name" : "french",
        "flag_emoji" : "🇫🇷"
    }

    def __str__(self):
        return f"{self.value['flag_emoji']} {self.value['full_name'].capitalize()}"