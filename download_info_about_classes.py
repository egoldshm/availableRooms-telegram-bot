import json
import requests
from config import *

FILE_NAME = FILENAME_ALL_DATA
headers = {
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'}
TryLogin = 'https://levnet.jct.ac.il/api/home/login.ashx?action=TryLogin'
CAMPUS = 1
YEAR = 5782
SEMESTER = 2
USERNAME = "egoldshm"


def get_info_from_string(time_and_place):
    STRING_TO_START = "כל השבועות - יום "
    if time_and_place == "":
        return [("", "", "", "", "")]

    else:
        result = []
        for part in time_and_place.split(STRING_TO_START)[1:]:
            day = part[:1]
            part = part[3:]
            start_time = part[0:5]
            end_time = part[6:11]
            build_and_room = part[13:].replace("\n", "")
            try:
                build = build_and_room.split(' ')[0]
                room = build_and_room.split(' ')[1]
                print(build + " " + room)
            except:
                build = build_and_room
                room = ""
            result.append((day, start_time, end_time, build, room))
        return result


def reload_file(username, password, year, semester, campus):
    login_data = {'username': username, "password": password}
    with requests.Session() as s:
        file = open(FILE_NAME, "w", encoding="utf-8")
        # file.write(",".join(context) + "\n")
        url = TryLogin
        url2 = "https://levnet.jct.ac.il/api/common/actualCourses.ashx?action=LoadActualCourses"
        url4 = "https://levnet.jct.ac.il/api/common/actualCourses.ashx?action=LoadActualCourse&ActualCourseID="
        r = s.post(url, data=login_data, headers=headers, verify=False)

        r = s.post(url2, data={"selectedAcademicYear": year, "selectedSemester": semester, "selectedExtension": campus},
                   headers=headers, verify=False)
        total_pages = json.loads(r.content)["totalPages"]
        for k in range(1, total_pages + 1):
            # r = s.get(url2, headers=headers)
            r = s.post(url2,
                       data={"selectedAcademicYear": year, "selectedSemester": semester, "selectedExtension": campus,
                             "selectedCategory": None, "freeSearch": None, "current": k}, headers=headers)
            items = json.loads(r.content)["items"]

            for i in items:
                url = url4 + str(i["id"])
                # r = s.get(url, headers=headers, verify = False)
                r = s.post(url, data=login_data, headers=headers, verify=False)
                result = json.loads(r.content)
                # print(result)
                if "groups" in result:
                    for j in result["groups"]:
                        time_and_place = str(j["courseGroupMeetings"])
                        for meet in get_info_from_string(time_and_place):
                            (day, start_time, end_time, build, room) = meet
                            arr = [i["id"], i["courseName"], j["groupFullNumber"], j["courseGroupLecturers"]
                                , day, start_time, end_time, build, room, str(j["groupTypeName"]),
                                   str(j["courseRelativeQuota"]), str(j["groupComment"])]
                            arr = [str(x).replace('\r', '').replace('\n', '').replace(",", ";").replace('"', "") for x
                                   in arr]
                            print(arr)
                            if time_and_place != "":
                                file.write(",".join(arr) + "\n")
        file.close()


def main():
    password = input("Enter password>\n")
    reload_file("egoldshm", password, year=YEAR, semester=SEMESTER, campus=CAMPUS)


def admin_update_file(message):
    _, password, year, semester, campus = message.split(" ")
    is_valid = True
    if year.isdigit():
        year = int(year)
    else:
        is_valid = False
    if semester.isdigit():
        semester = int(semester)
    else:
        is_valid = False
    if campus.isdigit():
        campus = int(campus)
    else:
        is_valid = False
    if not is_valid:
        return "הנתונים לא תקינים לעדכון"
    reload_file(USERNAME, password, year, semester, campus)
    return "בוצע עדכון נתונים"


if __name__ == "__main__":
    admin_update_file("עדכן  5779 2 1")
