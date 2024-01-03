from enum import Enum

DEVICE_KEY = "device"

class Devices(Enum):

    CPU = "cpu"
    CUDA = "cuda:%(gpu_id)d"
    #ROCM = "rocm"

    def with_id(self, gpu_id : int):
        if self == Devices.CUDA:
            return self.value % {"gpu_id" : gpu_id}
        else:
            return self.value