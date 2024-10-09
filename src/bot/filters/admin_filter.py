import telebot

class AdminFilter(telebot.custom_filters.SimpleCustomFilter):

    key: str = "admin_filter"
    admin_user : int = 0

    def __init__(self, admin_user_id):
        AdminFilter.admin_user = admin_user_id
    

    @staticmethod
    def check(message) -> bool:
        return True if message.from_user.id == AdminFilter.admin_user else False