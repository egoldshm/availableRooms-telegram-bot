# -*- coding: utf-8 -*-

from datetime import datetime, time
from time import strftime, gmtime
from typing import List, Any
import csv
import pytz
from config import *

IST = pytz.timezone('Etc/GMT-2')


def get_now() -> tuple:
    """
    get current time

    :return: tuple like (day in heb letter, HH:MM)
    """
    day = datetime.now(tz=IST).today().weekday()
    day = "בגדהוזא"[day]
    hour_min = datetime.now(tz=IST).strftime("%H:%M")
    return day, hour_min


def index_of(item):
    return context.index(item)


def room_of(i):
    return i[index_of("building")], i[index_of("room number")]


def get_data_from_file(file_path: str) -> str:
    """
    get file name of cvs file, and return the file as list of lists

    :param file_path: path of file
    :return: data as list of lists
    """
    with open(filepath, newline='\n', encoding='UTF-8') as csvfile:
        data = list(csv.reader(csvfile))
    data = list(filter(lambda i: i[index_of("building")] != "" and i[index_of("start time")] != "", data))
    return data


def is_time_between(begin_time, end_time, check_time=None):
    check_time = check_time or datetime.utcnow().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else:  # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def get_class_for_now(data, all_classes):
    now = get_now()
    return get_classes_by_time(data, all_classes, now[0], now[1])


def get_classes_by_time(data, all_classes, day, time):
    list_of_empty_rooms = []
    result = []
    for room in all_classes:
        if list(filter(lambda i: i[index_of("day")] == day and room_of(i) == room
                                 and is_time_between(i[index_of("start time")], i[index_of("end time")], time),
                       data)) == []:
            list_of_empty_rooms.append(room)
    for room in list_of_empty_rooms:
        lesson_today_in_room = list(
            filter(lambda i: room_of(i) == room and i[index_of("day")] == day and i[index_of("start time")] > time,
                   data))
        if len(lesson_today_in_room) == 0:
            soon_time = "סוף היום 💪"
        else:
            sorted_list = sorted(lesson_today_in_room, key=lambda i: i[index_of("start time")])
            soon_time = sorted_list[0][index_of("start time")]
        result.append(room + (soon_time,))
    return result


def day_and_hour(i):
    return i[index_of("day")], i[index_of("start time")]


def sort_list_by_time(data, day=None, hour_min=None):
    if day == None or hour_min == None:
        (day, hour_min) = get_now()
    # list1 = sorted(filter(
    #    lambda i: day > i[index_of("day")] or day == i[index_of("day")] and hour_min >= i[index_of("start time")],
    #    data), key=day_and_hour)
    # list2 = sorted(filter(lambda i: i not in list2, data), key=day_and_hour)
    # return list1 + list2
    return sorted(data, key=day_and_hour)
