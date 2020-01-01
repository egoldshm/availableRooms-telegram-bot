# -*- coding: utf-8 -*-

filepath = "קורסים.csv"
context = ["id", "course name", "course code", "teacher", "day",
           "start time", "end time", "build", "room number", "type", "students number", "notes"]
import time


def isTimeFormat(input):
    try:
        time.strptime(input, '%H:%M')
        return True
    except ValueError:
        return False
