from enum import Enum

TASK_KEY = "task"

class Tasks(Enum):
    TRANSCRIBE = "transcribe"
    TRANSLATE = "translate"

    @classmethod
    def list_names(cls):
        return [i.name for i in Tasks]
    
    @classmethod
    def list_values(cls):
        return [i.value for i in Tasks]



class TasksDescription(Enum):
    TRANSCRIBE = {
        "full_name" : "transcribe",
        "task_emoji" : "✍"
    }

    TRANSLATE = {
        "full_name" : "translate",
        "task_emoji" : "🗣"
    }

    def __str__(self):
        return f"{self.value['task_emoji']} {self.value['full_name'].capitalize()}"
