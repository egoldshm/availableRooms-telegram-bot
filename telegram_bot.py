# -*- coding: utf-8 -*-
import os
from typing import Dict

from download_info_about_classes import admin_update_file
from empty_classes import *
import logging
from telegram.ext import Updater, MessageHandler, Filters
from telegram import KeyboardButton, ReplyKeyboardMarkup

import report_file
user_info: Dict[str, str]
users_want_only_labs: Dict[str, str]
users_select: Dict[str, str]

PORT = int(os.environ.get('PORT', 8443))
d = available_classes()
users_info = {}
users_want_only_labs = {}
users_select = {}


def list_of_lists_to_keyboards(buttons: List[List[str]]) -> ReplyKeyboardMarkup:
    result_buttons = []
    for row in buttons:
        result_row = []
        for button in row:
            result_row.append(KeyboardButton(button))
        result_buttons.append(result_row)
    return ReplyKeyboardMarkup(result_buttons)


def start(update, context):
    """
    An event-triggered function when a user activates the bot
    """
    keyboard = get_keyboard("", update.message.from_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE, reply_markup=keyboard)
    report_file.report_to_file(context, update.message.date, update.message.from_user.id,
                               update.message.from_user.first_name,
                               str(update.message.from_user.last_name), str(update.message.from_user.username),
                               update.message.text)


def send_to_admin(update, context):
    user = update.message.from_user
    result = """
    הודעה חדשה 📢
    מזהה: {}
    שם: {} 
    שם אחרון: {}
    שם משתמש: {}
     
     
     {}""".format(user.id, user.first_name, user.last_name, user.username, update.message.text)
    context.bot.send_message(ADMIN_ID, result)


def answer_in_bot(update, context):
    """
    An event-triggered function that answers the user's response to a bot
    """
    message = update.message.text
    result = answer(message, update.message.from_user.id)
    if result[0] == "ToAdmin":
        send_to_admin(update, context)
        result = result[1]

    check = report_file.get_file_by_req(update, context)
    if check:
        result = check

    keyboard = get_keyboard(message, update.message.from_user.id)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=keyboard)
    report_file.report_to_file(context, update.message.date, update.message.from_user.id,
                               update.message.from_user.first_name,
                               str(update.message.from_user.last_name), str(update.message.from_user.username),
                               update.message.text)


def add_return_buttons(lst):
    return [[COMMAND_RETURN]] + lst + [
        [COMMAND_RETURN]]


def get_heb_letters_by_list(lst, letters_in_line=5):
    print(lst)
    letters = [i for i in HEB_LETTERS if
               i in list(map(lambda j: len(j) > 0 and j[0], map(lambda j: j.replace(" ", ""), lst)))]
    result = [[COMMAND_SHOW_ALL]]
    for i in range(0, len(letters) + 1, letters_in_line):
        result.append([j for j in letters[i + letters_in_line - 1:i - 1 if i > 0 else None: -1]])
    return add_return_buttons(result)


def get_keyboard(message, user_id):
    """
    A function that returns the keyboard for a user's message
    """
    if message == COMMAND_BY_ROOM:
        buildinges = sorted(list(set([i[0] for i in d.classes])))
        result = add_return_buttons([[i] for i in buildinges])
    elif message in list(map(lambda i: i[0], d.classes)):
        result = add_return_buttons([[i[0] + " " + i[1]] for i in d.classes if i[0] == message])
    elif message == COMMAND_BY_SUBJECT:
        users_select[user_id] = COMMAND_BY_SUBJECT
        result = get_heb_letters_by_list(d.subjects)
    elif message == COMMAND_BY_TEACHER:
        users_select[user_id] = COMMAND_BY_TEACHER
        result = get_heb_letters_by_list(d.teachers)
    elif message == COMMAND_FINDED_MISTAKE:
        result = [[COMMAND_RETURN]]
    elif message == COMMAND_SHOW_ALL:
        option = users_select[user_id]
        if option == COMMAND_BY_SUBJECT:
            result = d.subjects
        elif option == COMMAND_BY_TEACHER:
            result = d.teachers
        result = add_return_buttons([[i] for i in result])
        users_select[user_id] = None
    elif message in HEB_LETTERS and users_select[user_id] in (COMMAND_BY_SUBJECT, COMMAND_BY_TEACHER):
        option = users_select[user_id]
        if option == COMMAND_BY_SUBJECT:
            lst = d.subjects
        elif option == COMMAND_BY_TEACHER:
            lst = d.teachers
        users_select[user_id] = None
        result = add_return_buttons(
            [[i] for i in lst if len(i) > 0 and i.replace(" ", "")[0] == message])
    else:
        result = [[COMMAND_BY_HOUR],
                  [COMMAND_EMPTY_ROOM_NOW],
                  [COMMAND_BY_ROOM, COMMAND_BY_TEACHER,
                   COMMAND_BY_SUBJECT],
                  [COMMAND_FINDED_MISTAKE],
                  [
                      COMMAND_ONLY_COMPUTERS if not user_id in users_want_only_labs else COMMAND_ALL_ROOMS],
                  [COMMAND_AGUDA],
                  [COMMAND_ABOUT]]
    return list_of_lists_to_keyboards(result)


def answer(message, user):
    """
    Reply to the bot according to the message
    """
    reply = d.answer_to_message(message, user in users_want_only_labs)
    if reply:
        result = reply
    elif COMMAND_FINDED_MISTAKE == message:
        result = RESULT_MISTAKE
        users_info[user] = COMMAND_FINDED_MISTAKE
    elif user in users_info and users_info[user] == COMMAND_FINDED_MISTAKE:
        result = COMMAND_SENED_MISTAKE
        users_info[user] = ""
        result = ("ToAdmin", result)
    elif user == ADMIN_ID and len(message.split(" ")) == 5 and message.split(" ")[0] == "עדכן":
        result = admin_update_file(message)
        d.__init__()
    else:
        users_info[user] = ""
        result = "פקודה לא נמצאה, נסה שנית 😞"
    if COMMAND_ONLY_COMPUTERS == message:
        users_want_only_labs[user] = COMMAND_ONLY_COMPUTERS
    elif COMMAND_ALL_ROOMS == message:
        del users_want_only_labs[user]

    return result




def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(API_CODE_OF_BOT, use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text & Filters.chat_type.private, answer_in_bot))
    dp.add_handler(MessageHandler(Filters.command, start))
    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=API_CODE_OF_BOT,
                          webhook_url=URL + API_CODE_OF_BOT)

    updater.idle()


if __name__ == "__main__":
    main()
