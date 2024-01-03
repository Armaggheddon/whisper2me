from enum import Enum

MODEL_NAME_KEY = "model_name"

class ModelNames(Enum):

    TINY = "tiny"
    TINY_EN = "tiny.en"
    BASE = "base"
    BASE_EN = "base.en"
    SMALL = "small"
    SMALL_EN = "small.en"
    MEDIUM = "medium"
    MEDIUM_EN = "medium.en"
    LARGE_V1 = "large-v1"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"
    LARGE = "large"

    @classmethod
    def get_names(cls):
        return [i.name for i in ModelNames]
    
    @classmethod
    def get_values(cls):
        return [i.value for i in ModelNames]