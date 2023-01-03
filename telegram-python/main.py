#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import re
import os
import pyqrcode
import base64


def generate_qr_code(address):
    qr_code = pyqrcode.create(address)
    qr_code_data = qr_code.png_as_base64_str(scale=5)
    return qr_code_data


from telegram import CallbackGame, KeyboardButton, WebAppInfo, __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 5):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import (
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
    InlineQueryResultGame,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    InlineQueryHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Withdraw States
(
    WITHDRAW__SELECT_CURRENCY,
    WITHDRAW__INPUT_AMOUNT,
    WITHDRAW__INPUT_WITHDRAW_ADDRESS,
    WITHDRAW__CONFIRMATION,
) = range(4)

from Keyboards import MAIN_MENU_RK, CONFIRMATION_IK, WITHDRAW_RK, GAMES_RK

from dotenv import load_dotenv


load_dotenv()  # take environment variables from .env.

TOKEN = os.getenv("TELEGRAM_API_KEY")
FRONTEND_BASE_URL = os.getenv("FRONTEND_BASE_URL")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display Start Reply Keyboard."""

    await update.message.reply_text(
        "Welcome Back to Lunaroll! 🎲",
        reply_markup=ReplyKeyboardMarkup(
            MAIN_MENU_RK(),
            resize_keyboard=True,
            input_field_placeholder="Main Menu",
        ),
    )

    return


async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show user's balances and input keyboard."""
    # user = update.message.from_user
    # logger.info("Gender of %s: %s", user.first_name, update.message.text)
    await update.message.reply_text(
        "Balances:\n\nUSDT: 1000.00",
        reply_markup=ReplyKeyboardMarkup(
            WITHDRAW_RK(),
            resize_keyboard=True,
            input_field_placeholder="Select Currency...",
        ),
    )
    await update.message.reply_text("Select currency to withdraw:")

    return WITHDRAW__SELECT_CURRENCY


async def withdraw_select_currency(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:

    # Perform regex
    if not re.match(r"^[a-zA-Z0-9]+$", update.message.text):
        # Send error message to user
        await update.message.reply_text(
            "Invalid Currency. Please try again.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return WITHDRAW__SELECT_CURRENCY

    # Store input in context
    context.user_data["currency"] = update.message.text
    logger.info("Currency: %s", update.message.text)

    await update.message.reply_text(
        "Input amount to withdraw:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return WITHDRAW__INPUT_AMOUNT


async def withdraw_input_amount(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:
    # Perform regex
    if not re.match(r"^\d+(\.\d{1,5})?$", update.message.text):
        # Send error message to user
        await update.message.reply_text(
            "Invalid Amount. Please try again.",
            reply_markup=ReplyKeyboardRemove(),
        )
        return WITHDRAW__INPUT_AMOUNT

    # Store input in context
    context.user_data["amount"] = update.message.text
    logger.info("Amount: %s", update.message.text)

    await update.message.reply_text(
        "Input address to withdraw:",
        reply_markup=ReplyKeyboardRemove(),
    )
    return WITHDRAW__INPUT_WITHDRAW_ADDRESS


async def withdraw_input_withdraw_address(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:

    regex = r"^0x[a-fA-F0-9]{40}$"
    if not re.match(regex, update.message.text):
        await update.message.reply_text(
            "Invalid Ethereum address. Please enter a valid address."
        )
        return WITHDRAW__INPUT_WITHDRAW_ADDRESS

    address = update.message.text
    context.user_data["withdraw_address"] = address
    logger.info("Withdraw Address: %s", update.message.text)
    await update.message.reply_text(
        f"""Confirm Withdrawal?\n\n{"{:.5f}".format(float(context.user_data['amount']))} {context.user_data['currency']} to {address}""",
        reply_markup=CONFIRMATION_IK(),
    )
    return WITHDRAW__CONFIRMATION


async def withdraw_confirmation(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> int:

    query = update.callback_query

    logger.info("Query Data: %s", query.data)

    if query.data == "withdraw_yes":
        await update.effective_message.reply_text(
            text="Withdrawal Confirmed",
            reply_markup=ReplyKeyboardMarkup(
                MAIN_MENU_RK(),
                resize_keyboard=True,
                input_field_placeholder="Main Menu",
            ),
        )
        await update.effective_message.edit_reply_markup()

    elif query.data == "withdraw_no":
        await update.effective_message.reply_text(
            text="Withdrawal Cancelled",
            reply_markup=ReplyKeyboardMarkup(
                MAIN_MENU_RK(),
                resize_keyboard=True,
                input_field_placeholder="Main Menu",
            ),
        )
        await update.effective_message.edit_reply_markup()

    return ConversationHandler.END


# Deposit States


async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    address = "0xCa5cF03D081197BE24eF707081FbD7F3F11EB02D"
    await update.message.reply_markdown_v2(
        f"Your Deposit Address: `{address}`",
    )

    # Generate QR Code
    qr_code_data = generate_qr_code(address)
    print(qr_code_data)

    # Send photo
    await update.message.reply_photo(
        photo=base64.b64decode(qr_code_data),
        caption="Scan to deposit",
    )


async def register(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Registered!",
    )


async def games(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        f"Choose your game 👇!",
        reply_markup=ReplyKeyboardMarkup(
            GAMES_RK(),
            resize_keyboard=True,
            input_field_placeholder="Select Game...",
        ),
    )


async def game_dice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    logger.info("Game Dice")
    await update.message.reply_game(
        game_short_name="dice",
    )


async def handle_game_callbacks(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> None:
    query = update.callback_query

    if query.game_short_name == "dice":
        await query.answer(url=FRONTEND_BASE_URL + "/dice")


async def inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.inline_query.query

    results = [InlineQueryResultGame(id="dice", game_short_name="dice")]
    await update.inline_query.answer(results)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(TOKEN).build()

    # Handle start

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    start_handler = CommandHandler("start", start)
    back_handler = MessageHandler(filters.Regex("^Back to Main Menu$"), start)
    register_handler = MessageHandler(filters.Regex("^📝 Register$"), register)
    games_handler = MessageHandler(filters.Regex("^🎲 Games$"), games)
    withdraw_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^💸 Withdraw$"), withdraw)],
        states={
            WITHDRAW__SELECT_CURRENCY: [
                MessageHandler(filters.TEXT, withdraw_select_currency)
            ],
            WITHDRAW__INPUT_AMOUNT: [
                MessageHandler(filters.TEXT, withdraw_input_amount),
            ],
            WITHDRAW__INPUT_WITHDRAW_ADDRESS: [
                MessageHandler(
                    filters.TEXT,
                    withdraw_input_withdraw_address,
                ),
            ],
            WITHDRAW__CONFIRMATION: [CallbackQueryHandler(withdraw_confirmation)],
        },
        fallbacks=[CommandHandler("cancel", cancel), CommandHandler("start", start)],
    )
    deposit_handler = MessageHandler(filters.Regex("^💰 Deposit$"), deposit)
    game_dice_handler = MessageHandler(filters.Regex("^▶️ Dice$"), game_dice)

    # Handle Launching URL
    games_callback_handler = CallbackQueryHandler(handle_game_callbacks)

    # Inline Query Handler (Games Search Inline)
    inline_query_handler = InlineQueryHandler(inline_query)

    # ADDING HANDLERS TO BOT

    # Basic Command Handlers
    application.add_handler(start_handler)
    application.add_handler(back_handler)
    application.add_handler(games_handler)
    application.add_handler(register_handler)
    application.add_handler(withdraw_handler)
    application.add_handler(deposit_handler)

    # Individual Games Handlers
    application.add_handler(game_dice_handler)

    # Games Callback Handler
    application.add_handler(games_callback_handler)

    # Inline Query Handler
    application.add_handler(inline_query_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
