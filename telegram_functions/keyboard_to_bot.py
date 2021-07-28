from typing import List

from telegram import ReplyKeyboardMarkup, KeyboardButton


def keyboard_to_bot(buttons: List[List[str]]) -> ReplyKeyboardMarkup:
    result_buttons = []
    for row in buttons:
        result_row = []
        for button in row:
            result_row.append(KeyboardButton(button))
        result_buttons.append(result_row)
    return ReplyKeyboardMarkup(result_buttons)