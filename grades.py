import csv
from config import STATISTICS_COURSES_FILE
courses_data = None

context = ["num", "id", "name", "year", "semester", "group", "credit",
           "category", "min_grade", "total_avg", "mid","avg_of_pass",
           "num_of_stud","num_of_pass", "60-64","65-69","70-74","75-79","80-84","85-89","90-94","95-100","fails", "passed"]
def index(item):
    context.index(item)


class statistics_courses(object):
    def __init__(self):
        self.start_year = None
        self.end_year = None
        self.course_name = None
        self.semester = None
        self.group_number = None
        self.category = None
        global courses_data
        if not courses_data:
            with open(STATISTICS_COURSES_FILE, newline='\n', encoding='UTF-8') as csvfile:
                courses_data = list(csv.reader(csvfile))
        self.result = courses_data
        
    def get_only_relevant_items(self):
        if self.start_year:
            self.result = list(filter(lambda i: i[index("year")] >= self.start_year, self.result))
        if self.end_year:
            self.result = list(filter(lambda i: i[index("year")] <= self.end_year, self.result))
        if self.course_name:
            self.result = list(filter(lambda i: i[index("name")] == self.course_name, self.result))
        if self.semester:
            self.result = list(filter(lambda i: i[index("semester")] == self.semester, self.result))
        if self.group_number:
            self.result = list(filter(lambda i: i[index("group")] == self.group_number, self.result))
        if self.group_number:
            self.result = list(filter(lambda i: i[index("category")] == self.category, self.result))
        return self.result

    def get_all_course_name(self):
        self.get_only_relevant_items()
        return sorted(list(set([item[index("name")] for item in self.result])))

    def get_all_semester(self):
        self.get_only_relevant_items()
        return sorted(list(set([item[index("semester")] for item in self.result])))

    def get_all_groups(self):
        self.get_only_relevant_items()
        return sorted(list(set([item[index("group")] for item in self.result])))

    def get_all_years(self):
        self.get_only_relevant_items()
        return sorted(list(set([item[index("year")] for item in self.result])))

    def get_all_category(self):
        self.get_only_relevant_items()
        return sorted(list(set([item[index("category")] for item in self.result])))
