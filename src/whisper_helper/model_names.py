from enum import Enum

MODEL_NAME_KEY = "model_name"

class ModelNames(Enum):

    TINY_EN = "tiny.en"
    TINY = "tiny"
    BASE_EN = "base.en"
    BASE = "base"
    SMALL_EN = "small.en"
    SMALL = "small"
    MEDIUM_EN = "medium.en"
    MEDIUM = "medium"
    LARGE_V1 = "large-v1"
    LARGE_V2 = "large-v2"
    LARGE_V3 = "large-v3"
    LARGE = "large"
    LARGE_TURBO_V3 = "large-turbo-v3"
    TURBO = "turbo"

    @classmethod
    def get_names(cls):
        return [i.name for i in ModelNames]
    
    @classmethod
    def get_values(cls):
        return [i.value for i in ModelNames]