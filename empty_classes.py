# -*- coding: utf-8 -*-

from typing import List, Any, Tuple
from config import *
from tools import get_now, index_of, room_of, is_time_between, get_data_from_file, get_computer_labs, compare, \
    sort_list_by_time, list_to_string, items_from_data, isTimeFormat


class available_classes(object):
    data: List
    classes: List[str]
    subjects: List[str]
    teachers: List[str]
    computer_labs: List[Tuple[str, str]]

    def __init__(self):
        self.data = get_data_from_file()
        self.classes = self.get_all_classes()
        self.subjects = self.get_all_subjects()
        self.teachers = self.get_all_teachers()
        self.computer_labs = get_computer_labs()

    def get_class_for_now(self, only_computers_room):
        now = get_now()
        return self.get_classes_by_time(now[0], now[1], only_computers_room)

    def get_all_classes(self) -> list:
        """
        get all classes in jct from data list

        :param data: list of lists with all data
        :return: list of tuples like (building, room number)
        """
        return sorted(list(set(map(lambda i: (i[index_of("building")], i[index_of("room number")]), self.data))),
                      key=lambda i: (i[0], i[1]))

    def get_all_teachers(self) -> list:
        """
        get all lecturers in jct from data list

        :type data: list of lists with all data
        :rtype: list
        :return: list of string with all lecturers
        """
        return sorted(list(set(map(lambda i: i[index_of("teacher")], self.data))))

    def get_all_subjects(self):
        """
        get all courses in jct from data list

        :type data: list of lists with all data
        :rtype: list
        :return: list of string with all courses
        """
        return sorted(list(set(map(lambda i: i[index_of("course name")], self.data))))

    def get_by_teacher(self, name):
        """
        Gets all data by a lecturer, in one long string form

        :param data: list of lists with the data
        :param name: The lecturer he wants to get the data
        :return: Long string with all data on the lecturer
        """
        lst = sort_list_by_time(filter(lambda i: compare(i[index_of("teacher")], name), self.data))
        return list_to_string('🎓 ', items_from_data(lst, "course name", "📅 יום", "day",
                                                     "start time", "end time", "🔹", "building", "room number", "type",
                                                     "students number", "notes"))

    def get_by_subject(self, subject):
        """
        Gets all data by a courses, in one long string form

        :param subject: The courses he wants to get the data
        :return: Long string with all data on the courses
        """
        lst = sort_list_by_time(filter(lambda i: i[index_of("course name")] == subject, self.data))
        return list_to_string('🎓 ', items_from_data(lst, "teacher", "📅 יום", "day",
                                                     "start time", "end time", "🔹", "building", "room number", "type",
                                                     "students number", "notes"))

    def get_by_room(self, building, room_number):
        """
        Gets all data by a building and room_number, in one long string form

        :param building, room_number: The room he wants to get the data
        :return: Long string with all data on the courses
        """
        lst = sort_list_by_time((filter(lambda i: room_of(i) == (building, room_number), self.data)))
        return list_to_string('🏘 ', items_from_data(lst, "course name", "teacher", "📅 יום", "day",
                                                     "start time", "end time", "🔹", "type",
                                                     "students number", "notes"))

    def get_only_computers_rooms(self, rooms):
        return [i for i in rooms if i[:2] in self.computer_labs]

    def rooms_to_string(self, rooms):
        """
        Gets a list of tuples - building, room, and when room is available, making it a readable string

        :param rooms: list of tuples - building, room, and when room is available
        :return: one long string
        """
        rooms = sorted(rooms, key=lambda i: (i[0], i[1]))
        rooms = map(lambda i: (i[0], i[1] + " (🖥)", i[2]) if i[:2] in self.computer_labs else i, rooms)
        return list_to_string("🆓 ", map(lambda i: i[0] + " " + i[1] + ", פנוי עד " + i[2], rooms))

    def get_classes_by_time(self, day, time, only_computers_room):
        list_of_empty_rooms = []
        result = []
        for room in self.classes:
            # get list for room with all lesson that now in the class
            if not list(filter(lambda i: i[index_of("day")] == day and room_of(i) == room and is_time_between(
                    i[index_of("start time")], i[index_of("end time")], time), self.data)):
                # if list is empty -> add room to list
                list_of_empty_rooms.append(room)

        # pass all room that found like a empty and add the soon lesson
        for room in list_of_empty_rooms:
            lesson_today_in_room = list(
                filter(lambda i: room_of(i) == room and i[index_of("day")] == day and i[index_of("start time")] > time,
                       self.data))
            if len(lesson_today_in_room) == 0:
                # if no lesson today after time
                soon_time = "סוף היום 💪"
            else:
                # if exist lessons today -> add first one
                sorted_list = sorted(lesson_today_in_room, key=lambda i: i[index_of("start time")])
                soon_time = sorted_list[0][index_of("start time")]
            result.append(room + (soon_time,))
        if only_computers_room:
            result = self.get_only_computers_rooms(result)
        return self.rooms_to_string(result)

    def answer_to_message(self, message, only_computers_room):
        if message == COMMAND_EMPTY_ROOM_NOW:
            result = " חדרים פנויים לעכשיו  😎:\n\n"
            result += self.get_class_for_now(only_computers_room)
        elif message == COMMAND_SHOW_ALL:
            result = RESULT_SHOW_ALL
        elif message in HEB_LETTERS:
            result = RESULT_BY_LETTER
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
        elif message == COMMAND_ABOUT:
            result = RESULT_ABOUT
        elif message == COMMAND_ALL_ROOMS:
            result = RESULT_ALL_ROOMS
        elif message == COMMAND_ONLY_COMPUTERS:
            result = RESULT_ONLY_COMPUTERS
        elif message == COMMAND_AGUDA:
            result = RESULT_AGUDA
        elif isTimeFormat(message):
            day = get_now()[0]
            result = result = "מציג חדרים פנויים עבור יום " + day + " " + message + " 😎:\n\n"
            result += self.get_classes_by_time(day, message, only_computers_room)
        elif message.split(" ")[0] in "אבגדהוז" and len(message.split(" ")) == 2 and isTimeFormat(
                message.split(" ")[1]):
            result = "מציג חדרים פנויים עבור יום " + message + " 😎:\n\n"
            result += self.get_classes_by_time(message.split(" ")[0], message.split(" ")[1], only_computers_room)
        elif len(list(filter(lambda i: compare(i, message), self.teachers))) == 1:
            result = "מציג את כל המידע על המרצה " + message + "\n\n"
            result += self.get_by_teacher(message)
        elif message in self.subjects:
            result = "מציג את כל המידע על הקורס  " + message + "\n\n"
            result += self.get_by_subject(message)
        elif message in [i[0] for i in self.classes]:
            result = RESULT_BY_ROOM1

        elif len(message.split(" ")) == 2 and (message.split(" ")[0], message.split(" ")[1]) in self.classes:
            result = "מציג את כל המידע על הכיתה " + message + "\n\n"
            result += self.get_by_room(message.split(" ")[0], message.split(" ")[1])
        else:
            result = False
        return result


if __name__ == "__main__":
    x = available_classes()
    print(x.get_all_classes())