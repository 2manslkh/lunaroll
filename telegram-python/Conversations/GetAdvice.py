from utils import (
    clean_up_question,
    make_intent_readable,
    group_by_intent,
    make_intent_readable_markdown,
)
from Conversations import Start
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackContext,
    CallbackQueryHandler,
)
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ParseMode,
)
from Behaviour import TakoBehaviour
import Keyboards
import MessageTemplates
import FirestoreEngine as fs
from ConversationEngine import AdviceHandler
import logging

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


INTENT_CACHE = fs.get_all_intents()

INPUT_QUESTION, INPUT_RATING, VIEW_COMMUNITY_ADVICE = range(3)

# === USER ASK ADVICE CONVERSATION START


def ask_advice(update: Update, context: CallbackContext) -> int:
    logger.info(f"User Selected: {update.message.text}")
    update.message.reply_text(
        "Ask me anything!",
        reply_markup=ReplyKeyboardRemove(),
    )

    return INPUT_QUESTION


def input_question(update: Update, context: CallbackContext) -> int:

    global Q_COUNT
    user = update.message.from_user
    user_id = user.id
    session_id = user.id
    language_code = "en-US"
    message = update.message.text
    logger.info(f"User Asked: {update.message.text}")

    if "bot_behaviour" not in context.chat_data:
        context.chat_data["bot_behaviour"] = TakoBehaviour()

    # Engage Dialogflow
    response = AdviceHandler.detect_intent_texts(
        session_id=session_id,
        texts=[message],
        language_code=language_code,
    )

    if response != None:

        # Check if small talk or not
        if response["action"].split(".")[0] == "smalltalk":

            # Reply with small talk
            update.message.reply_text(
                f"{utils.make_intent_readable(response['action'])}:\n{response['fulfillment_text']}"
            )
            update.message.reply_text(
                f"Ask me question instead! {context.chat_data['bot_behaviour'].get_sass()}",
            )

            # Make bot sassier
            context.chat_data["bot_behaviour"].increase_anger()

            # Remain in same state
            return INPUT_QUESTION

        # Check if Default Fallback Intent
        if response["action"] == "input.unknown":

            # Reply with Default Fallback fulfillment text
            update.message.reply_text(
                f"{utils.make_intent_readable(response['intent'])}:\n{response['fulfillment_text']}"
            )
            update.message.reply_text(
                f"Ask me another question!",
            )

            # Remain in same state
            return INPUT_QUESTION

        else:

            response_text = response["fulfillment_text"]

            # Check if there is a fulfillment text
            if response_text:

                # Store Advice in Database
                if response["intent"] not in INTENT_CACHE:
                    advice_id = fs.add_advice(
                        response_text, response["intent"])
                    INTENT_CACHE.append(advice_id)
                    context.chat_data["advice_id"] = advice_id
                    fs.add_intent(response["intent"])
                else:
                    context.chat_data["advice_id"] = fs.get_advice_id(
                        response_text)

                # Reply with a fulfillment text and intent (for debugging)
                update.message.reply_text(
                    f"{make_intent_readable(response['intent'])}:\n{response_text}"
                )

                # Check if end of conversation
                if response["end"]:

                    # TODO: Need to identify what are the useful questions to store
                    # Store Question to Database
                    doc_ref = fs.add_question(
                        user_id,
                        question_text=clean_up_question(
                            message
                        ),  # clean question before storing in DB
                        intent=response["intent"],
                    )

                    # Only ask for rating if its a request dating advice or a question
                    if response["intent"].split(".")[0] in [
                        "datingadvice",
                        "question",
                        "replyadvice",
                    ]:

                        # Store intent in context
                        context.chat_data["question_intent"] = response["intent"]

                        # Ask user for feedback
                        update.message.reply_text(
                            "Was it good advice?",
                            reply_markup=ReplyKeyboardMarkup(
                                Keyboards.REPLY_KEYBOARD_2(), one_time_keyboard=True
                            ),
                        )

                        # Move to next state
                        return INPUT_RATING

                else:
                    # Remain in same state
                    return INPUT_QUESTION
            else:
                update.message.reply_text(
                    f"{response['intent']}:\nSorry I don't have an answer for that now!"
                )
                update.message.reply_text(
                    f"Ask me another question!",
                )
                # Remain in same state
                return INPUT_QUESTION
    else:
        update.message.reply_text("Sorry there has been an Error!")
        update.message.reply_text(
            f"Ask me another question!",
        )
        # Remain in same state
        return INPUT_QUESTION


def input_rating(update: Update, context: CallbackContext) -> int:
    """Get user's rating for given advice

    Args:
        update (Update):
        context (CallbackContext):

    Returns:
        int: Transition to next state
    """

    vote = update.message.text
    session_id = update.message.from_user.id
    language_code = "en-US"
    advice_id = context.chat_data["advice_id"]
    # Engage Dialogflow

    results = AdviceHandler.detect_intent_texts(
        session_id=session_id,
        texts=[vote],
        language_code=language_code,
    )

    if results != None:
        logger.info(f"User voted: {make_intent_readable(results['intent'])}")
        if results["intent"] in ["statement.yes", "statement.no"]:

            if results["intent"] == "statement.yes":
                fs.upvote_advice(advice_id)

            keyboard = Keyboards.INLINE_KEYBOARD_1()

            update.message.reply_text(
                "Thank you! Would you like to view more advice from the community?",
                reply_markup=InlineKeyboardMarkup(
                    Keyboards.INLINE_KEYBOARD_1()),
            )

            return VIEW_COMMUNITY_ADVICE

        else:

            update.message.reply_text(
                "I'm Sorry. Was it good advice? Yes or No you idiot.",
            )

    else:
        update.message.reply_text("Sorry there has been an Error!")

    return INPUT_RATING


def view_ca_button(update: Update, context: CallbackContext) -> int:
    query = update.callback_query

    user_id = query.from_user.id

    # Questions Key
    i = query.data

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    # Retrieve questions intent from context
    question_intent = context.chat_data["question_intent"]

    logger.info(f"User Selected Option: {i}")

    if i == "View Community Advice":
        community_advice = fs.get_community_advices_by_intent(question_intent)
        context.chat_data["community_advice"] = {
            ca["uid"]: ca for ca in community_advice
        }
        if len(community_advice) > 0:
            query.edit_message_text(
                text=f"*Here are some advice given by the community:*",
                parse_mode=ParseMode.MARKDOWN_V2,
            )

            for j in range(len(community_advice)):
                query.message.reply_text(
                    MessageTemplates.COMMUNITY_ADVICE_MESSAGE_BLOCK.format(
                        advice_text=community_advice[j]["advice_text"],
                        points=community_advice[j]["points"],
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        Keyboards.INLINE_KEYBOARD_2(community_advice[j]["uid"])
                    ),
                )
        else:
            query.edit_message_text(
                text=f"*There are no advice given by the community yet\!*",
                parse_mode=ParseMode.MARKDOWN_V2,
                reply_markup=InlineKeyboardMarkup(
                    Keyboards.INLINE_KEYBOARD_3()),
            )

    elif i == "Back to Profile":

        # Remove inline markup
        query.message.edit_text(
            text="Thank you! Would you like to view more advice from the community?",
            reply_markup=None,
        )

        # Show Profile
        Start.show_profile(user_id, query)
        logger.info("Conversation Ended")
        return ConversationHandler.END

    return VIEW_COMMUNITY_ADVICE


def input_ca_rating(update: Update, context: CallbackContext) -> int:
    query = update.callback_query
    logger.info(query)
    if query.data == "Back to Profile":
        return ConversationHandler.END

    # Questions Key
    i = query.data.split(".")
    advice_id = i[0]
    action = i[1]

    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery
    query.answer()

    community_advice = context.chat_data["community_advice"]

    if action == "up":
        fs.upvote_community_advice(advice_id)
        logger.info(f"User Upvoted: Advice ID ({advice_id})")
        query.edit_message_text(
            MessageTemplates.COMMUNITY_ADVICE_MESSAGE_BLOCK.format(
                advice_text=community_advice[advice_id]["advice_text"],
                points=community_advice[advice_id]["points"] + 1,
            ),
            reply_markup=None,
        )

    elif action == "down":
        fs.downvote_community_advice(advice_id)
        logger.info(f"User Downvoted Advice ID ({advice_id})")
        query.edit_message_text(
            MessageTemplates.COMMUNITY_ADVICE_MESSAGE_BLOCK.format(
                advice_text=community_advice[advice_id]["advice_text"],
                points=community_advice[advice_id]["points"] - 1,
            ),
            reply_markup=None,
        )

    elif action == "report":
        # TODO: Add report function
        logger.info(f"User Reported Advice ID ({advice_id})")
        query.edit_message_text(
            text="Thank you for reporting!",
            reply_markup=None,
        )


# USER ASK ADVICE CONVERSATION END ===


def cancel(update: Update, context: CallbackContext) -> int:
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


conversation = ConversationHandler(
    entry_points=[
        MessageHandler("^(Ask for Advice \U00002753)$", ask_advice)
    ],
    states={
        INPUT_QUESTION: [
            MessageHandler(
                Filters.text
                & ~Filters.regex("^(Ask for Advice \U00002753|Give Advice \U0001F4A1)$")
                & ~Filters.command,
                input_question,
            )
        ],
        INPUT_RATING: [MessageHandler(Filters.text & ~Filters.command, input_rating)],
        VIEW_COMMUNITY_ADVICE: [CallbackQueryHandler(view_ca_button)],
    },
    fallbacks=[
        CommandHandler("cancel", cancel),
        # MessageHandler(Filters.regex("^(Ask for Advice \U00002753)$"), ask_advice),
        # MessageHandler(Filters.regex("^(Give Advice \U0001F4A1)$"), give_advice),
        # MessageHandler(Filters.regex("^(Texting Advice \U0000265F)$"), texting_advice),
    ],
)
