from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def MAIN_MENU_RK():
    return [["📝 Register", "💰 Deposit", "💸 Withdraw"]]


def WITHDRAW_IK():
    return [[InlineKeyboardButton("USDT", callback_data="withdraw_usdt")]]


def CONFIRMATION_IK():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Yes", callback_data="withdraw_confirm")],
            [InlineKeyboardButton("No", callback_data="withdraw_cancel")],
        ]
    )
