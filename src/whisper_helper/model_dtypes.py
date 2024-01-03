from enum import Enum

DTYPE_KEY = "use_fp16"

class ModelDtypes(Enum):

    FP32 = False
    FP16 = True