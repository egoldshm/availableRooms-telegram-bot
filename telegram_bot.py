# -*- coding: utf-8 -*-
from empty_classes import *
import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup

# constants:
WELCOME_MESSAGE = """ברוך הבא! בחר אופציה מהתפריט ⬇😎"""

COMMAND_EMPTY_ROOM_NOW = 'חדרים פנויים עכשיו ⏳'
COMMAND_BY_HOUR = 'לפי זמן ספיציפי ⏰'
COMMAND_BY_ROOM = 'מידע על חדר 🏠'
COMMAND_BY_TEACHER = 'מידע לפי מרצה 👨‍🏫'
RESULT_BY_TEACHER = "בחר מרצה מהרשימה, או הקלד את השם המלא במדוייק ⬇"

COMMAND_BY_SUBJECT = 'מידע לפי קורס 🎓'
RESULT_BY_SUBJECT = "בחר קורס מהרשימה, או הקלד את השם המלא במדוייק ⬇"

RESULT_BY_ROOM = "בחר חדר מהרשימה, או הקלד בניין ומספר ⬇"
RESULT_FOR_BY_HOUR = """אחלה,
שלח יום ושעה בפורמט של '<יום> HH:MM'
לדוגמה - א 15:15
"""


def get_all_classes(data):
    return sorted(list(set(map(lambda i: (i[index_of("build")], i[index_of("room number")]), data))),
                  key=lambda i: (i[0], i[1]))


def get_all_teachers(data):
    return sorted(list(set(map(lambda i: i[index_of("teacher")], data))))


def get_all_subjects(data):
    return sorted(list(set(map(lambda i: i[index_of("course name")], data))))


def items_from_data(lst, *info):
    return list(map(lambda i: " ".join([(i[index_of(item)] if item in context else item) for item in info]), lst))


def list_to_string(string, lst):
    x = "\n" + string + " "
    y = x.join(lst)
    return string + y


def get_by_teacher(data, name):
    lst = sort_list_by_time(filter(lambda i: compare(i[index_of("teacher")], name), data))
    return list_to_string('🎓 ', items_from_data(lst, "course name", "📅 יום", "day",
                                                 "start time", "end time", "🔹", "build", "room number", "type",
                                                 "students number", "notes"))


def get_by_subject(data, subject):
    lst = sort_list_by_time(filter(lambda i: i[index_of("course name")] == subject, data))
    return list_to_string('🎓 ', items_from_data(lst, "teacher", "📅 יום", "day",
                                                 "start time", "end time", "🔹", "build", "room number", "type",
                                                 "students number", "notes"))


def get_by_room(data, build, room_number):
    lst = sort_list_by_time((filter(lambda i: room_of(i) == (build, room_number), data)))
    return list_to_string('🏘 ', items_from_data(lst, "course name", "teacher", "📅 יום", "day",
                                                 "start time", "end time", "🔹", "type",
                                                 "students number", "notes"))


def start(update, context):
    kb = get_keyboard("")
    kb_markup = ReplyKeyboardMarkup(kb)
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE, reply_markup=kb_markup)
    

def rooms_to_string(rooms):
    rooms = sorted(rooms, key=lambda i: (i[0], i[1]))
    return list_to_string("🆓 ", map(lambda i: i[0] + " " + i[1] + ", פנוי עד " + i[2], rooms))


def answer_in_bot(update, context):
    message = update.message.text
    result = answer(message)
    kb = get_keyboard(message)
    kb_markup = ReplyKeyboardMarkup(kb)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=kb_markup)


def get_keyboard(message):
    if message == COMMAND_BY_ROOM:
        result = list(map(lambda i: [KeyboardButton(i[0] + " " + i[1])], classes))
    elif message == COMMAND_BY_SUBJECT:
        result = list(map(lambda i: [KeyboardButton(i)], subjects))
    elif message == COMMAND_BY_TEACHER:
        result = list(map(lambda i: [KeyboardButton(i)], teachers))
    else:
        result = [[KeyboardButton(COMMAND_BY_HOUR)],
                  [KeyboardButton(COMMAND_EMPTY_ROOM_NOW)],
                  [KeyboardButton(COMMAND_BY_ROOM), KeyboardButton(COMMAND_BY_TEACHER),
                   KeyboardButton(COMMAND_BY_SUBJECT)]]
    return result


def answer(message):
    if message == COMMAND_EMPTY_ROOM_NOW:
        result = " חדרים פנויים לעכשיו  😎:\n\n"
        result += rooms_to_string(get_class_for_now(data, classes))
    elif message == COMMAND_BY_HOUR:
        result = RESULT_FOR_BY_HOUR
    elif message == COMMAND_BY_ROOM:
        result = RESULT_BY_ROOM
    elif message == COMMAND_BY_SUBJECT:
        result = RESULT_BY_SUBJECT
    elif message == COMMAND_BY_TEACHER:
        result = RESULT_BY_TEACHER
    elif message.split(" ")[0] in "אבגדהו" and isTimeFormat(message.split(" ")[1]):
        result = "מציג חדרים פנויים עבור יום " + message + " 😎:\n\n"
        result += rooms_to_string(get_classes_by_time(data, classes, message.split(" ")[0], message.split(" ")[1]))
    elif len(list(filter(lambda i: compare(i, message), teachers))) == 1:
        result = "מציג את כל המידע על המרצה " + message + "\n\n"
        result += get_by_teacher(data, message)
    elif message in subjects:
        result = "מציג את כל המידע על הקורס  " + message + "\n\n"
        result += get_by_subject(data, message)
    elif len(message.split(" ")) == 2 and (message.split(" ")[0], message.split(" ")[1]) in classes:
        result = "מציג את כל המידע על הכיתה " + message + "\n\n"
        result += get_by_room(data, message.split(" ")[0], message.split(" ")[1])
    else:
        result = "פקודה לא נמצאה, נסה שנית 😞"
    return result


data = get_data_from_file(filepath)
classes = get_all_classes(data)
subjects = get_all_subjects(data)
teachers = get_all_teachers(data)

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
updater = Updater(token='1028809311:AAGr-JzIAGItdtpeX6WUAPquGdzlMmIyENE', use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
echo_handler = MessageHandler(Filters.text, answer_in_bot)
dispatcher.add_handler(echo_handler)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
