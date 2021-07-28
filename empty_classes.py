# -*- coding: utf-8 -*-

from typing import List, Any, Tuple, Dict
from config import *
from config import COMMAND_BY_ROOM, COMMAND_BY_SUBJECT, COMMAND_BY_TEACHER, COMMAND_FINDED_MISTAKE, COMMAND_RETURN, \
    COMMAND_SHOW_ALL, HEB_LETTERS, COMMAND_BY_HOUR, COMMAND_EMPTY_ROOM_NOW, COMMAND_ONLY_COMPUTERS, COMMAND_ALL_ROOMS, \
    COMMAND_AGUDA, COMMAND_ABOUT, RESULT_MISTAKE, COMMAND_SENED_MISTAKE, ADMIN_ID
from download_info_about_classes import admin_update_file
from telegram_bot import d
from tools import get_now, index_of, room_of, is_time_between, get_data_from_file, get_computer_labs, compare, \
    sort_list_by_time, list_to_string, items_from_data, is_time_format


def add_return_buttons(lst: List[List[str]]) -> List[List[str]]:
    return [[COMMAND_RETURN]] + lst + [
        [COMMAND_RETURN]]


def get_heb_letters_by_list(lst: List[List[str]], letters_in_line=5) -> List[List[str]]:
    print(lst)
    letters = [i for i in HEB_LETTERS if
               i in list(map(lambda j: len(j) > 0 and j[0], map(lambda j: j.replace(" ", ""), lst)))]
    result = [[COMMAND_SHOW_ALL]]
    for i in range(0, len(letters) + 1, letters_in_line):
        result.append([j for j in letters[i + letters_in_line - 1:i - 1 if i > 0 else None: -1]])
    return add_return_buttons(result)


class AvailableClasses:
    data: List
    classes: List[Tuple[str, str]]
    subjects: List[str]
    teachers: List[str]
    computer_labs: List[Tuple[str, str]]

    user_info: Dict[str, str]
    users_want_only_labs: Dict[str, str]
    users_select: Dict[str, str]

    def __init__(self):
        self.data = get_data_from_file()
        self.classes = self.get_all_classes()
        self.subjects = self.get_all_subjects()
        self.teachers = self.get_all_teachers()
        self.computer_labs = get_computer_labs()

        self.users_info = {}
        self.users_want_only_labs = {}
        self.users_select = {}

    def get_class_for_now(self, only_computers_room: bool) -> str:
        now = get_now()
        return self.get_classes_by_time(now[0], now[1], only_computers_room)

    def get_all_classes(self) -> List[Tuple[str, str]]:
        """
        get all classes in jct from data list

        :param data: list of lists with all data
        :return: list of tuples like (building, room number)
        """
        return sorted(list(set(map(lambda i: (i[index_of("building")], i[index_of("room number")]), self.data))),
                      key=lambda i: (i[0], i[1]))

    def get_all_teachers(self) -> List[str]:
        """
        get all lecturers in jct from data list

        :type data: list of lists with all data
        :return: list of string with all lecturers
        """
        return sorted(list(set(map(lambda i: i[index_of("teacher")], self.data))))

    def get_all_subjects(self) -> List[str]:
        """
        get all courses in jct from data list

        :type data: list of lists with all data
        :rtype: list
        :return: list of string with all courses
        """
        return sorted(list(set(map(lambda i: i[index_of("course name")], self.data))))

    def get_by_teacher(self, name: str) -> str:
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

    def get_by_subject(self, subject: str) -> str:
        """
        Gets all data by a courses, in one long string form

        :param subject: The courses he wants to get the data
        :return: Long string with all data on the courses
        """
        lst = sort_list_by_time(filter(lambda i: i[index_of("course name")] == subject, self.data))
        return list_to_string('🎓 ', items_from_data(lst, "teacher", "📅 יום", "day",
                                                     "start time", "end time", "🔹", "building", "room number", "type",
                                                     "students number", "notes"))

    def get_by_room(self, building: str, room_number: str) -> str:
        """
        Gets all data by a building and room_number, in one long string form

        :param building:
        :param room_number: The room he wants to get the data
        :return: Long string with all data on the courses
        """
        lst = sort_list_by_time((filter(lambda i: room_of(i) == (building, room_number), self.data)))
        return list_to_string('🏘 ', items_from_data(lst, "course name", "teacher", "📅 יום", "day",
                                                     "start time", "end time", "🔹", "type",
                                                     "students number", "notes"))

    def get_only_computers_rooms(self, rooms: List[Tuple[str, str, str]]) -> List[Tuple[str, str, str]]:
        return [i for i in rooms if i[:2] in self.computer_labs]

    def rooms_to_string(self, rooms_and_times: List[Tuple[str, str, str]]) -> str:
        """
        Gets a list of tuples - building, room, and when room is available, making it a readable string

        :param rooms_and_times: list of tuples - building, room, and when room is available
        :return: one long string
        """
        rooms = sorted(rooms_and_times, key=lambda i: (i[0], i[1]))
        rooms = map(lambda i: (i[0], i[1] + " (🖥)", i[2]) if i[:2] in self.computer_labs else i, rooms)
        return list_to_string("🆓 ", map(lambda i: i[0] + " " + i[1] + ", פנוי עד " + i[2], rooms))

    def get_classes_by_time(self, day: str, time: str, only_computers_room: bool) -> str:
        list_of_empty_rooms: List[Tuple[str, str]]
        result: List[Tuple[str, str, str]]
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

    def answer_to_message(self, message: str, only_computers_room: bool) -> str:
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
        elif is_time_format(message):
            day = get_now()[0]
            result = result = "מציג חדרים פנויים עבור יום " + day + " " + message + " 😎:\n\n"
            result += self.get_classes_by_time(day, message, only_computers_room)
        elif message.split(" ")[0] in "אבגדהוז" and len(message.split(" ")) == 2 and is_time_format(
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

    def get_keyboard(self, message: str, user_id) -> List[List[str]]:
        """
        A function that returns the keyboard for a user's message
        """
        if message == COMMAND_BY_ROOM:
            buildinges = sorted(list(set([i[0] for i in d.classes])))
            result = add_return_buttons([[i] for i in buildinges])
        elif message in list(map(lambda i: i[0], d.classes)):
            result = add_return_buttons([[i[0] + " " + i[1]] for i in d.classes if i[0] == message])
        elif message == COMMAND_BY_SUBJECT:
            self.users_select[user_id] = COMMAND_BY_SUBJECT
            result = get_heb_letters_by_list(d.subjects)
        elif message == COMMAND_BY_TEACHER:
            self.users_select[user_id] = COMMAND_BY_TEACHER
            result = get_heb_letters_by_list(d.teachers)
        elif message == COMMAND_FINDED_MISTAKE:
            result = [[COMMAND_RETURN]]
        elif message == COMMAND_SHOW_ALL:
            option = self.users_select[user_id]
            if option == COMMAND_BY_SUBJECT:
                result = d.subjects
            elif option == COMMAND_BY_TEACHER:
                result = d.teachers
            result = add_return_buttons([[i] for i in result])
            self.users_select[user_id] = None
        elif message in HEB_LETTERS and self.users_select[user_id] in (COMMAND_BY_SUBJECT, COMMAND_BY_TEACHER):
            option = self.users_select[user_id]
            if option == COMMAND_BY_SUBJECT:
                lst = d.subjects
            elif option == COMMAND_BY_TEACHER:
                lst = d.teachers
            self.users_select[user_id] = None
            result = add_return_buttons(
                [[i] for i in lst if len(i) > 0 and i.replace(" ", "")[0] == message])
        else:
            result = [[COMMAND_BY_HOUR],
                      [COMMAND_EMPTY_ROOM_NOW],
                      [COMMAND_BY_ROOM, COMMAND_BY_TEACHER,
                       COMMAND_BY_SUBJECT],
                      [COMMAND_FINDED_MISTAKE],
                      [
                          COMMAND_ONLY_COMPUTERS if not user_id in self.users_want_only_labs else COMMAND_ALL_ROOMS],
                      [COMMAND_AGUDA],
                      [COMMAND_ABOUT]]
        return result

    def answer(s, message: str, user) -> str:
        """
        Reply to the bot according to the message
        """
        reply = d.answer_to_message(message, user in s.users_want_only_labs)
        if reply:
            result = reply
        elif COMMAND_FINDED_MISTAKE == message:
            result = RESULT_MISTAKE
            s.users_info[user] = COMMAND_FINDED_MISTAKE
        elif user in s.users_info and s.users_info[user] == COMMAND_FINDED_MISTAKE:
            result = COMMAND_SENED_MISTAKE
            s.users_info[user] = ""
            result = ("ToAdmin", result)
        elif user == ADMIN_ID and len(message.split(" ")) == 5 and message.split(" ")[0] == "עדכן":
            result = admin_update_file(message)
            d.__init__()
        else:
            s.users_info[user] = ""
            result = "פקודה לא נמצאה, נסה שנית 😞"
        if COMMAND_ONLY_COMPUTERS == message:
            s.users_want_only_labs[user] = COMMAND_ONLY_COMPUTERS
        elif COMMAND_ALL_ROOMS == message:
            del s.users_want_only_labs[user]

        return result


if __name__ == "__main__":
    x = AvailableClasses()
    print(x.get_all_classes())
