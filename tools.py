# -*- coding: utf-8 -*-
import csv
import time
import re
from datetime import datetime, time
from time import strftime, gmtime, strptime

from config import COMPUTER_LABS_FILE, FILENAME_ALL_DATA, context, HEB_LETTERS


def get_now() -> tuple:
    """
    get current time

    :return: tuple like (day in heb letter, HH:MM)
    """
    from config import IST
    day = datetime.now(tz=IST).today().weekday()
    day = "בגדהוזא"[day]
    hour_min = datetime.now(tz=IST).strftime("%H:%M")
    return day, hour_min


def isTimeFormat(input):
    try:
        strptime(input, '%H:%M')
        return True
    except ValueError:
        return False


def compare(a, b):
    """
    Compare two base strings, disregarding whitespace
    """
    return re.sub("\s*", "", a) == re.sub("\s*", "", b)


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


def index_of(item):
    from config import context
    return context.index(item)


def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def room_of(i):
    return i[index_of("building")], i[index_of("room number")]


def day_and_hour(i):
    return i[index_of("day")], i[index_of("start time")]


def sort_list_by_time(data, day=None, hour_min=None):
    """
    get list and sort by start time and day
    :param data: list of lists in format of context
    :param day: day to sort (not in use)
    :param hour_min: (not in use)
    :return: sorted list
    """
    #
    if day is None or hour_min is None:
        (day, hour_min) = get_now()
    # list1 = sorted(filter(
    #    lambda i: day > i[index_of("day")] or day == i[index_of("day")] and hour_min >= i[index_of("start time")],
    #    data), key=day_and_hour)
    # list2 = sorted(filter(lambda i: i not in list2, data), key=day_and_hour)
    # return list1 + list2
    return sorted(data, key=day_and_hour)


def get_data_from_file(file_path: str = FILENAME_ALL_DATA) -> list:
    """
    get file name of cvs file, and return the file as list of lists

    :param file_path: path of file
    :return: data as list of lists
    """
    with open(file_path, newline='\n', encoding='UTF-8') as csvfile:
        data = list(csv.reader(csvfile))
    # take only what have building and start time
    return list(filter(lambda i: i[index_of("building")] != "" and i[index_of("start time")] != "", data))


def get_computer_labs(file_path=COMPUTER_LABS_FILE):
    f = open(file_path, "r", encoding='UTF-8')
    return list(
        map(lambda i: (i.split(" ")[0], i.split(" ")[1]), map(lambda i: i.replace("\n", ""), f.readlines())))



