import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)

from ConversationEngine import AdviceHandler
import FirestoreEngine as fs
import Keyboards

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

SELECT_QUESTION, ANSWER_QUESTION = range(2)

# === USER GIVE ADVICE CONVERSATION START
def give_advice(update: Update, context: CallbackContext) -> int:

    keyboard = []

    # Output messages initialization
    question_text = "*Select a question to give advice\!*\n\n"

    # Get Questions from Database
    questions = fs.get_questions()

    questions_grouped = group_by_intent(questions)
    context.chat_data["questions_cache"] = questions

    if len(questions) == 0:
        update.message.reply_text(
            f"There are no questions yet!",
        )
        return ConversationHandler.END

    else:

        # counter = 1
        for key in questions_grouped.keys():

            # Group set of questions by intent
            question_text += f"*{make_intent_readable_markdown(key)}*:\n"

            # Get unique questions only
            unique_questions = list(set(questions_grouped[key]))

            for question in unique_questions:
                question_text += f"    \- {question}\n"

            question_text += "\n"
            keyboard.append(
                [InlineKeyboardButton(make_intent_readable(key), callback_data=key)]
            )
            # counter += 1

        reply_markup = InlineKeyboardMarkup(keyboard)

        update.message.reply_markdown_v2(
            f"{question_text}",
            reply_markup=reply_markup,
        )

    return SELECT_QUESTION


def answer_question_button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query

    # Questions Key
    i = query.data

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    # Retrieve questions from cache
    questions = context.chat_data["questions_cache"]

    logger.info(f"User Selected question intent: {i}")
    query.edit_message_text(
        text=f"*Selected option:* {make_intent_readable_markdown(i)}",
        parse_mode=ParseMode.MARKDOWN_V2,
    )

    query.message.reply_text(
        "Give your response below:",
        reply_markup=ReplyKeyboardRemove(),
    )

    # Store intent in cache for next state
    context.chat_data["current_question_intent"] = i

    return ANSWER_QUESTION


def answer_question(update: Update, context: CallbackContext) -> None:
    global A_COUNT
    user_id = update.message.from_user.id
    advice = update.message.text

    question_intent = f"{context.chat_data['current_question_intent']}"
    logger.info(f"User gave advice: {advice}")
    context.chat_data["current_question_intent"] = ""

    # Check if advice is similar to current advices
    response = AdviceHandler.detect_intent_texts(
        session_id=user_id,
        texts=[advice],
        language_code="en-US",
    )

    logger

    # Check if under current question intent, there is no existing advice intent
    if question_intent not in response["intent"] or question_intent:
        # TODO: Create new intent with given input as training phrase
        count = fs.get_unique_advice_intent_count(question_intent)
        advice_intent = f"{question_intent}.ca.{count}"
        AdviceHandler.add_new_intent(advice_intent, advice)

    # Store Advice in Database
    fs.add_community_advice(user_id, advice, question_intent, advice_intent)

    update.message.reply_text(
        "Thank you for your advice!",
        reply_markup=ReplyKeyboardMarkup(
            Keyboards.REPLY_KEYBOARD_1(), one_time_keyboard=True
        ),
    )

    return ConversationHandler.END


# USER GIVE ADVICE CONVERSATION END ===


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


conversation = ConversationHandler(
    entry_points=[
        CommandHandler("giveadvice", give_advice),
        MessageHandler(Filters.regex("^(Give Advice \U0001F4A1)$"), give_advice),
    ],
    states={
        SELECT_QUESTION: [
            # MessageHandler(Filters.text & ~Filters.command, answer_question),
            CallbackQueryHandler(answer_question_button),
        ],
        ANSWER_QUESTION: [
            MessageHandler(Filters.text & ~Filters.command, answer_question),
        ],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        # MessageHandler(Filters.regex("^(Ask for Advice \U00002753)$"), ask_advice),
        # MessageHandler(Filters.regex("^(Give Advice \U0001F4A1)$"), give_advice),
        # MessageHandler(Filters.regex("^(Texting Advice \U0000265F)$"), texting_advice),
    ],
)
