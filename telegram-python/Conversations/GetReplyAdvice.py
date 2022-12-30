import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

from ConversationEngine import ReplyHandler

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

from utils import (
    clean_up_question,
    make_intent_readable,
    group_by_intent,
    make_intent_readable_markdown,
)

INPUT_REPLY_MESSAGE = range(1)

# ===============   TEXTING ADVICE START
def texting_advice(update: Update, context: CallbackContext) -> None:

    message = update.message.text
    session_id = update.message.from_user.id
    language_code = "en-US"

    # Engage Dialogflow
    results = ReplyHandler.detect_intent_texts(
        session_id=session_id,
        texts=[message],
        language_code=language_code,
    )

    update.message.reply_text(f"{results['fulfillment_text']}")

    is_end = results["end"]

    if not is_end:
        return INPUT_REPLY_MESSAGE
    else:
        return ConversationHandler.END


# TEXTING ADVICE END  ===============


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


conversation = ConversationHandler(
    entry_points=[
        CommandHandler("textingadvice", texting_advice),
        MessageHandler(Filters.regex("^(Texting Advice \U0000265F)$"), texting_advice),
    ],
    states={
        INPUT_REPLY_MESSAGE: [
            MessageHandler(Filters.text & ~Filters.command, texting_advice),
        ]
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        # MessageHandler(Filters.regex("^(Ask for Advice \U00002753)$"), ask_advice),
        # MessageHandler(Filters.regex("^(Give Advice \U0001F4A1)$"), give_advice),
        # MessageHandler(Filters.regex("^(Texting Advice \U0000265F)$"), texting_advice),
    ],
)
