import telebot


class UserFilter(telebot.custom_filters.SimpleCustomFilter):
    key: str = "user_filter"
    allowed_users  = list()
    admin_id = 0

    def __init__(self, admin_id, allowed_users ):
        UserFilter.admin_id = admin_id
        UserFilter.allowed_users = allowed_users

    @staticmethod
    def check(message) -> bool:
        return True if message.from_user.id in UserFilter.allowed_users or message.from_user.id == UserFilter.admin_id else False