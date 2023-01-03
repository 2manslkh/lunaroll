from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def MAIN_MENU_RK():
    return [["📝 Register", "💰 Deposit", "💸 Withdraw"], ["🎲 Games"]]


def WITHDRAW_RK():
    return [["USDT", "USDC", "WBTC", "WETH"]]


def GAMES_RK():
    return [["▶️ Dice"]]


def WITHDRAW_IK():
    return [[InlineKeyboardButton("USDT", callback_data="withdraw_usdt")]]


def CONFIRMATION_IK():
    return InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Yes", callback_data="withdraw_yes")],
            [InlineKeyboardButton("No", callback_data="withdraw_no")],
        ]
    )
