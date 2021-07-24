# -*- coding: utf-8 -*-
from empty_classes import *
import logging
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler
from telegram import KeyboardButton, ReplyKeyboardMarkup

import report_file

# Constants - for messages:
WELCOME_MESSAGE = """ברוכה הבאה! בחרי אופציה מהתפריט ⬇😎"""
ADMIN_ID = 114534171

COMMAND_EMPTY_ROOM_NOW = 'חדרים פנויים עכשיו ⏳'
RESULT_RETURN = "אוקיי, חזרתי!"
COMMAND_BY_HOUR = 'לפי זמן ספיציפי ⏰'
RESULT_FOR_BY_HOUR = """אחלה,
שלחי יום ושעה בפורמט של '<יום> HH:MM'
לדוגמה - א 15:15
"""

COMMAND_BY_ROOM = 'מידע על חדר 🏠'
RESULT_BY_ROOM = "בחרי חדר מהרשימה, או הקלדי בניין ומספר ⬇"

COMMAND_BY_TEACHER = 'מידע לפי מרצה 👨‍🏫'
RESULT_BY_TEACHER = "בחרי מרצה מהרשימה, או הקלדי את השם המלא במדוייק ⬇"

COMMAND_BY_SUBJECT = 'מידע לפי קורס 🎓'
RESULT_BY_SUBJECT = "בחרי קורס מהרשימה, או הקלדי את השם המלא במדוייק ⬇"

COMMAND_RETURN = "חזור 🔙"
COMMAND_FINDED_MISTAKE = "רעיון לשיפור? 🔎 רוצה לפרגן? 🤗 מצאת טעות? 😟"
COMMAND_ABOUT = "אודות הבוט 🤖"
RESULT_ABOUT = """הבוט נכתב במהלך חבורתא בסיבוכיות 🙈 ע"י @eitanttt.

הקוד כתוב בפייתון, רוצה לקבל אותו? 💻 בשמחה! דבר איתי. (חינם אין כסף, כמובן)"""
RESULT_MISTAKE = """רעיון לשיפור? 🔎 רוצה לפרגן? 🤗 איזה כיף😃 אתה יכול לכתוב כאן!

מצאת טעות במערכת? 😟 מתנצל על עוגמת הנפש, טעות לעולם חוזר וכו'...
הנתונים נלקחים מהלב נט, ויש פעמים שהם לא הכי מעודכנים בעולם 😔
אבל אל דאגה! יחד אנחנו נבנה מאגר טוב יותר ומעודכן יותר! 💪
אנא כתבי לי - במילים חופשיות - על הטעות שמצאת.
ובעז"ה אני אעבור על זה ואתקן 😇
תודה!"""

COMMAND_SENED_MISTAKE = "קיבלתי, תודה!😁"
# end constants - for messages
USERS = {}




def items_from_data(lst, *info) -> object:
    """
    Receives a list in the form of DATA and according to the data sent in INFO decides how to display them, and what to display.

    :param lst: list of list in "DATA" format
    :param info: list Which contains descriptions of columns in DATA and also just strings to display in the result
    :return: list of strings
    """
    return list(map(lambda i: " ".join([(i[index_of(item)] if item in context else item) for item in info]), lst))


def list_to_string(string, lst):
    """
    Gets a string and list, and returns one long string - where each row is a row in the list - with the string between them

    :param string: A row-to-line separator will usually be emoji or any character.
    :param lst: List of strings
    :return: One long string
    """
    x = "\n" + string + " "
    y = x.join(lst)
    return string + " " + y


def get_by_teacher(name):
    """
    Gets all data by a lecturer, in one long string form

    :param data: list of lists with the data
    :param name: The lecturer he wants to get the data
    :return: Long string with all data on the lecturer
    """
    lst = sort_list_by_time(filter(lambda i: compare(i[index_of("teacher")], name), data))
    return list_to_string('🎓 ', items_from_data(lst, "course name", "📅 יום", "day",
                                                 "start time", "end time", "🔹", "building", "room number", "type",
                                                 "students number", "notes"))


def get_by_subject(subject):
    """
    Gets all data by a courses, in one long string form

    :param subject: The courses he wants to get the data
    :return: Long string with all data on the courses
    """
    lst = sort_list_by_time(filter(lambda i: i[index_of("course name")] == subject, data))
    return list_to_string('🎓 ', items_from_data(lst, "teacher", "📅 יום", "day",
                                                 "start time", "end time", "🔹", "building", "room number", "type",
                                                 "students number", "notes"))


def get_by_room(building, room_number = None):
    """
    Gets all data by a building and room_number, in one long string form

    :param building, room_number: The room he wants to get the data
    :return: Long string with all data on the courses
    """
    lst = sort_list_by_time((filter(lambda i: room_of(i) == building, data)))
    return list_to_string('🏘 ', items_from_data(lst, "course name", "teacher", "📅 יום", "day",
                                                 "start time", "end time", "🔹", "type",
                                                 "students number", "notes"))


def start(update, context):
    """
    An event-triggered function when a user activates the bot
    """
    kb = get_keyboard("")
    kb_markup = ReplyKeyboardMarkup(kb)
    context.bot.send_message(chat_id=update.effective_chat.id, text=WELCOME_MESSAGE, reply_markup=kb_markup)
    report_file.report_to_file(context, update.message.date, update.message.from_user.id, update.message.from_user.first_name,
                               str(update.message.from_user.last_name), str(update.message.from_user.username),
                               update.message.text)


def rooms_to_string(rooms):
    """
    Gets a list of tuples - building, room, and when room is available, making it a readable string

    :param rooms: list of tuples - building, room, and when room is available
    :return: one long string
    """
    rooms = sorted(rooms)
    rooms = map(lambda i: i[0] + " (🖥)"+ i[1] if i[0] in computer_labs else i, rooms)
    return list_to_string("🆓 ", map(lambda i: i[0] + ", פנוי עד " + i[1], rooms))


def send_to_admin(update, context):
    result = "הודעה חדשה מ:\n"
    result += "id: " + str(
        update.message.from_user.id) + " first name: " + update.message.from_user.first_name + " last name: " + \
              str(update.message.from_user.last_name) + " username: " + str(update.message.from_user.username)
    result += "\n\n"
    result += update.message.text
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
    if check != False:
        result = check

    kb = get_keyboard(message)
    kb_markup = ReplyKeyboardMarkup(kb)
    context.bot.send_message(chat_id=update.effective_chat.id, text=result, reply_markup=kb_markup)
    report_file.report_to_file(context, update.message.date, update.message.from_user.id, update.message.from_user.first_name,
                               str(update.message.from_user.last_name), str(update.message.from_user.username),
                               update.message.text)


def add_return_buttons(lst):
    return [[KeyboardButton(COMMAND_RETURN)]] + lst + [
        [KeyboardButton(COMMAND_RETURN)]]


def get_keyboard(message):
    """
    A function that returns the keyboard for a user's message
    """
    if message == COMMAND_BY_ROOM:
        result = add_return_buttons(list(map(lambda i: [KeyboardButton(i)], classes)))
    elif message == COMMAND_BY_SUBJECT:
        result = add_return_buttons(list(map(lambda i: [KeyboardButton(i)], subjects)))
    elif message == COMMAND_BY_TEACHER:
        result = add_return_buttons(list(map(lambda i: [KeyboardButton(i)], teachers)))
    elif message == COMMAND_FINDED_MISTAKE:
        result = [[KeyboardButton(COMMAND_RETURN)]]
    else:
        result = [[KeyboardButton(COMMAND_BY_HOUR)],
                  [KeyboardButton(COMMAND_EMPTY_ROOM_NOW)],
                  [KeyboardButton(COMMAND_BY_ROOM), KeyboardButton(COMMAND_BY_TEACHER),
                   KeyboardButton(COMMAND_BY_SUBJECT)],
                  [KeyboardButton(COMMAND_FINDED_MISTAKE)],
                  [KeyboardButton(COMMAND_ABOUT)]]
    return result


def answer(message, user):
    """
    Reply to the bot according to the message
    """
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
    elif message == COMMAND_RETURN:
        result = RESULT_RETURN
    elif message == COMMAND_FINDED_MISTAKE:
        result = RESULT_MISTAKE
        USERS[user] = COMMAND_FINDED_MISTAKE
    elif message == COMMAND_ABOUT:
        result = RESULT_ABOUT
    elif message.split(" ")[0] in "אבגדהו" and isTimeFormat(message.split(" ")[1]):
        result = "מציג חדרים פנויים עבור יום " + message + " 😎:\n\n"
        result += rooms_to_string(get_classes_by_time(data, classes,message.split(" ")[0], message.split(" ")[1]))
    elif len(list(filter(lambda i: compare(i, message), teachers))) == 1:
        result = "מציג את כל המידע על המרצה " + message + "\n\n"
        result += get_by_teacher(message)
    elif message in subjects:
        result = "מציג את כל המידע על הקורס  " + message + "\n\n"
        result += get_by_subject(message)

    elif message in classes:
        result = "מציג את כל המידע על הכיתה " + message + "\n\n"
        result += get_by_room(message)
    elif user in USERS and USERS[user] == COMMAND_FINDED_MISTAKE:
        result = COMMAND_SENED_MISTAKE
        USERS[user] = ""
        result = ("ToAdmin", result)
    else:
        result = "פקודה לא נמצאה, נסה שנית 😞"
    return result

data = get_data_from_file(filepathTal)
classes = get_all_classes(data)
subjects = get_all_subjects(data)
teachers = get_all_teachers(data)
computer_labs = get_computer_labs()

if __name__ == "__main__":

    logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    updater = Updater(token='1006870809:AAEEwOdbCS13a6ZPVT5jkn-Evo9lN4LLpSo', use_context=True)
    dispatcher = updater.dispatcher
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
    echo_handler = MessageHandler(Filters.text, answer_in_bot)
    dispatcher.add_handler(echo_handler)
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)
    updater.start_polling()
