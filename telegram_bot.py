# -*- coding: utf-8 -*-
import os

from empty_classes import *
import logging
from telegram.ext import Updater, MessageHandler, Filters

from reporters import reporter
from telegram_functions.keyboard_to_bot import keyboard_to_bot
from telegram_functions.send_message_to_admin import send_to_admin

PORT = int(os.environ.get('PORT', 8443))
d = AvailableClasses()


def start(update, context):
    """
    An event-triggered function when a user activates the bot
    """
    keyboard = keyboard_to_bot(d.get_keyboard("", update.message.from_user.id))
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE, reply_markup=keyboard)
    reporter.report_to_file(context, update.message.date, update.message.from_user.id,
                            update.message.from_user.first_name,
                            str(update.message.from_user.last_name), str(update.message.from_user.username),
                            update.message.text)


def answer_in_bot(update, context):
    """
    An event-triggered function that answers the user's response to a bot
    """
    message = update.message.text
    user_id = update.message.from_user.id
    result = d.answer(message, user_id)
    if result[0] == "ToAdmin":
        send_to_admin(update, context)
        result = result[1]

    check = reporter.get_file_by_req(update, context)
    if check:
        result = check

    keyboard = keyboard_to_bot(d.get_keyboard(message, user_id))
    context.bot.send_message(chat_id=user_id, text=result, reply_markup=keyboard)
    reporter.report_to_file(context, update.message.date, user_id,
                            update.message.from_user.first_name,
                            str(update.message.from_user.last_name), str(update.message.from_user.username),
                            update.message.text)


def main():
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    updater = Updater(API_CODE_OF_BOT, use_context=True)
    dp = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

    dp.add_handler(MessageHandler(Filters.text & Filters.chat_type.private, answer_in_bot))
    dp.add_handler(MessageHandler(Filters.command, start))

    updater.start_webhook(listen="0.0.0.0",
                          port=int(PORT),
                          url_path=API_CODE_OF_BOT,
                          webhook_url=URL + API_CODE_OF_BOT)

    updater.idle()


if __name__ == "__main__":
    main()
