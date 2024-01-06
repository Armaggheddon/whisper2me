import telebot
from telebot import TeleBot

from filters.user_filter import UserFilter
from filters.admin_filter import AdminFilter
from handlers import (
    language_selector,
    start_command,
    task_selector,
    voice_message,
    remove_user,
    purge_users,
    add_user,
    list_users,
    not_admin,
    help_user,
    help_admin,
    info_command,
)

from storage import storage


def register_handlers(bot_handle : TeleBot):
    """Registers all the handlers for the bot
    """
    # Help command for users
    bot_handle.register_message_handler(
        help_user.handle_user_help_command,
        commands=[help_user.CMD],
        user_filter=True,
        admin_filter=False,
        pass_bot=True
    )

    # Help command for admin
    bot_handle.register_message_handler(
        help_admin.handle_admin_help_command,
        commands=[help_admin.CMD],
        admin_filter=True,
        pass_bot=True
    )


    # Start command handler
    bot_handle.register_message_handler(
        start_command.handle_start_command,
        commands=[start_command.CMD],
        user_filter=True,
        pass_bot = True,
    )

    # Voice message handler
    bot_handle.register_message_handler(
        voice_message.handle_voice_message,
        content_types = voice_message.CONTENT_TYPES,
        user_filter = True,
        pass_bot = True,
    )

    # Info command handler
    bot_handle.register_message_handler(
        info_command.handle_info_command,
        commands=[info_command.CMD],
        admin_filter=True,
        user_filter=True,
        pass_bot = True,
    )


    # Change language handler
    bot_handle.register_message_handler(
        language_selector.handle_language_command,
        commands=[language_selector.CMD],
        admin_filter=True,
        pass_bot = True,
    )
    bot_handle.register_callback_query_handler(
        language_selector.language_selection_cb,
        func= language_selector.CB_LAMBDA,
        pass_bot = True,
    )

    # Change task handler
    bot_handle.register_message_handler(
        task_selector.handle_task_command,
        commands=[task_selector.CMD],
        admin_filter=True,
        pass_bot = True,
    )
    bot_handle.register_callback_query_handler(
        task_selector.task_selection_cb,
        func= task_selector.CB_LAMBDA,
        pass_bot = True,
    )


    # List users handler
    bot_handle.register_message_handler(
        list_users.handle_list_users,
        commands=[list_users.CMD],
        admin_filter=True,
        pass_bot = True
    )

    # Add user handler
    bot_handle.register_message_handler(
        add_user.handle_user_add,
        commands=[add_user.CMD],
        admin_filter = True,
        pass_bot = True
    )

    # Remove user handler
    bot_handle.register_message_handler(
        remove_user.handle_user_remove,
        commands=[remove_user.CMD],
        admin_filter = True,
        pass_bot = True
    )
    bot_handle.register_callback_query_handler(
        remove_user.user_remove_selection_cb,
        func = remove_user.CB_LAMBDA,
        pass_bot = True
    )

    # Purge users handler
    bot_handle.register_message_handler(
        purge_users.handle_purge_command,
        commands=[purge_users.CMD],
        admin_filter=True,
        pass_bot=True
    )

    # Non admin handler
    bot_handle.register_message_handler(
        not_admin.handle_non_admin_endpoint,
        commands=[list_users.CMD, add_user.CMD, remove_user.CMD],
        admin_filter = False,
        user_filter = True,
        pass_bot = True
    )



def run(
    bot_token : str = storage.bot_token, 
    admin_id : int = storage.admin_id, 
    allowed_users = storage.allowed_users
):
    """Runs the bot with the given token and admin id
    
    Args:
    - bot_token : str - the token of the bot
    - admin_id : int - the admin id
    - allowed_users : list - the list of allowed users

    Arguments default to the values retrieved by storage
    """
    whisper_bot = TeleBot(bot_token)
    register_handlers(whisper_bot)
    whisper_bot.add_custom_filter(AdminFilter(admin_id))
    whisper_bot.add_custom_filter(UserFilter(admin_id, allowed_users))
    whisper_bot.infinity_polling()