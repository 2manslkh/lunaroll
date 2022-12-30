import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

from ConversationEngine import AdviceHandler
import FirestoreEngine as fs
import MessageTemplates
import Keyboards
from Behaviour import TakoBehaviour

from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ParseMode,
)
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)

PROFILE_CREATION, PROFILE_VIEW = range(2)
PROFILES_CACHE = fs.get_all_existing_users()


def start(update: Update, context: CallbackContext) -> None:

    """Start Command

    Starts the conversation with the bot.

    Checks if new user:

    If new user:

    Ask for user's name
    " How may I address you? "

    Else:

    Show user profile

    """

    user_id = update.message.from_user.id
    user_first_name = update.message.from_user.first_name

    update.message.reply_text(
        "Welcome to Dr. Tako Dating Advice \U0001F419",
    )

    if user_id in PROFILES_CACHE:
        logger.info(f"Returning user with id ({user_id}) has engaged the bot")
    else:
        update.message.reply_text(f"Hello there {user_first_name}. Nice to meet you!")
        logger.info(f"Creating new user with id: {user_id}")
        create_profile(user_id, user_first_name)

    # View Profile
    show_profile(user_id, update)

    return ConversationHandler.END


def show_profile(user_id: int, update: Update) -> None:
    # View Profile
    user_profile = fs.get_user(str(user_id)).to_dict()
    output = MessageTemplates.PROFILE_MESSAGE.format(**user_profile)

    update.message.reply_markdown_v2(
        output,
        reply_markup=ReplyKeyboardMarkup(
            Keyboards.REPLY_KEYBOARD_1(), one_time_keyboard=True
        ),
    )


def create_profile(user_id: int, user_first_name: str) -> None:

    global PROFILES_CACHE

    # Update profiles cache
    PROFILES_CACHE.append(user_id)

    # Add user to firestore
    fs.add_user(user_id, user_first_name)

    return None


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


conversation = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={},
    fallbacks=[
        CommandHandler("cancel", cancel),
    ],
)