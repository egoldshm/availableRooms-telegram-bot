# -*- coding: utf-8 -*-
from empty_classes import *
import logging
from telegram.ext import Updater
from telegram import KeyboardButton, ReplyKeyboardMarkup

# constants:
WELCOME_MESSAGE = """ברוך הבא! בחר אופציה מהתפריט ⬇😎"""

COMMAND_EMPTY_ROOM_NOW = 'חדרים פנויים עכשיו'
COMMAND_BY_HOUR = 'לפי זמן ספיציפי'
COMMAND_BY_ROOM = 'מידע על חדר'
RESULT_FOR_BY_HOUR = """אחלה,
שלח יום ושעה בפורמט של '<יום> HH:MM'
לדוגמה - א 15:15
"""

def start(update, context):
    kb = [[KeyboardButton(COMMAND_BY_HOUR)],
          [KeyboardButton(COMMAND_EMPTY_ROOM_NOW)],
          [KeyboardButton(COMMAND_BY_ROOM)]]
    kb_markup = ReplyKeyboardMarkup(kb)
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE, reply_markup=kb_markup)


logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

updater = Updater(token='--------', use_context=True)

dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
data = get_data_from_file(filepath)
classes = get_all_classes(data)


def rooms_to_string(rooms):
    rooms = sorted(rooms, key = lambda i: (i[0], i[1]))
    print(rooms)
    return "🆓 "+"\n🆓 ".join(map(lambda i: i[0] + " " + i[1] + ", פנוי עד " + i[2], rooms))


def answer(update, context):
    message = update.message.text
    if message == COMMAND_EMPTY_ROOM_NOW:
        result = " חדרים פנויים לעכשיו  😎:\n\n"
        result += rooms_to_string(get_class_for_now(data, classes))
    elif message == COMMAND_BY_HOUR:
        result = RESULT_FOR_BY_HOUR
    elif message == COMMAND_BY_ROOM:
        result = "הפקודה בשלבי בנייה. נא להמתין בסבלנות."
    elif message.split(" ")[0] in "אבגדהו" and isTimeFormat(message.split(" ")[1]):
        result = "מציג חדרים פנויים עבור " + message + " 😎:\n\n"
        result += rooms_to_string(get_classes_by_time(data, classes, message.split(" ")[0], message.split(" ")[1]))

    else:
        result = "פקודה לא נמצאה, נסה שנית 😞"

    context.bot.send_message(chat_id=update.effective_chat.id, text=result)


from telegram.ext import MessageHandler, Filters

echo_handler = MessageHandler(Filters.text, answer)
dispatcher.add_handler(echo_handler)

from telegram.ext import CommandHandler

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

updater.start_polling()
