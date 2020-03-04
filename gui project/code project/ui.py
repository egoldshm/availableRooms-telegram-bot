from sys import argv, exit

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QWidget, QScrollArea, QHBoxLayout, QVBoxLayout, QMainWindow)

import empty_classes
from config import IconPath
from tools import get_now


class MainWindow(QMainWindow):

    def __init__(self):
        self.d = empty_classes.available_classes()
        super().__init__()
        self.initUI()
        self.setWindowIcon(QtGui.QIcon(IconPath))

    def initUI(self):
        self.setWindowTitle("יש פה שיעור?")

        self.scroll = QScrollArea()  # Scroll Area which contains the widgets, set as the centralWidget
        self.widget = QWidget()  # Widget that contains the collection of Vertical Box
        self.vbox = QVBoxLayout()  # The Vertical Box that contains the Horizontal Boxes of  labels and buttons

        self.addButtons()
        self.add_events_to_buttons()
        self.update_current_time()

        self.widget.setLayout(self.vbox)

        # Scroll Area Properties
        self.scroll.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        self.scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll.setWidgetResizable(True)
        self.scroll.setWidget(self.widget)
        self.retranslateUi(self)
        self.setCentralWidget(self.scroll)

        self.setGeometry(30, 30, 1000, 500)
        self.setWindowTitle('יש פה שיעור??')
        self.show()

    def addButtons(self):
        # add button to show available classes now
        self.nowButton = QtWidgets.QPushButton("חדרים פנויים עכשיו")
        # self.nowButton.setGeometry(QRect(450, 10, 311, 61))
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(28)
        self.nowButton.setFont(font)
        self.nowButton.setObjectName("nowButton")
        self.vbox.addWidget(self.nowButton)

        # add combobox for select teacher/class/course
        self.comboBox = QtWidgets.QComboBox()
        # self.comboBox.setGeometry(QtCore.QRect(210, 80, 301, 61))
        self.comboBox.setObjectName("comboBox")
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(20)
        self.comboBox.setFont(font)
        self.comboBox.setEditable(True)
        self.comboBox.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

        # add button to show the data of teacher/class/course
        self.showInfoButton = QtWidgets.QPushButton("הצג מידע")
        self.showInfoButton.setGeometry(QtCore.QRect(4, 80, 192, 62))
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(20)
        self.showInfoButton.setFont(font)
        self.showInfoButton.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.showInfoButton.setObjectName("showInfoButton")
        self.showInfoButton.setEnabled(False)

        # add teachers to combobox
        self.showTeacherButton = QtWidgets.QPushButton()
        self.showTeacherButton.setGeometry(QtCore.QRect(520, 80, 241, 23))
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(10)
        self.showTeacherButton.setFont(font)
        self.showTeacherButton.setObjectName("showTeacherButton")

        # add classes to combobox
        self.showClassesButton = QtWidgets.QPushButton()
        self.showClassesButton.setGeometry(QtCore.QRect(520, 100, 241, 23))
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(10)
        self.showClassesButton.setFont(font)
        self.showClassesButton.setObjectName("showClassesButton")

        # add courses to combobox
        self.showCoursesButton = QtWidgets.QPushButton()
        self.showCoursesButton.setGeometry(QtCore.QRect(520, 120, 241, 23))
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(10)
        self.showCoursesButton.setFont(font)
        self.showCoursesButton.setObjectName("showCoursesButton")

        layoutOfOptions = QHBoxLayout()
        layoutOfOptions.addWidget(self.comboBox)
        layoutOfOptions.addWidget(self.showInfoButton)
        layout_of_3button = QVBoxLayout()
        layout_of_3button.addWidget(self.showCoursesButton)
        layout_of_3button.addWidget(self.showClassesButton)
        layout_of_3button.addWidget(self.showTeacherButton)
        widget2 = QWidget()
        widget2.setLayout(layout_of_3button)
        layoutOfOptions.addWidget(widget2)
        widget1 = QWidget()
        widget1.setLayout(layoutOfOptions)
        self.vbox.addWidget(widget1)

        self.timeEdit = QtWidgets.QTimeEdit()
        self.timeEdit.setGeometry(QtCore.QRect(220, 10, 131, 61))
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(24)
        self.timeEdit.setFont(font)
        self.timeEdit.setAccessibleName("")
        self.timeEdit.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.timeEdit.setAlignment(QtCore.Qt.AlignCenter)
        self.timeEdit.setObjectName("timeEdit")

        self.days = QtWidgets.QComboBox()
        self.days.setGeometry(QtCore.QRect(360, 10, 81, 61))
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(16)
        self.days.setFont(font)
        self.days.setCurrentText("")
        self.days.setObjectName("days")

        self.days.setEditable(True)
        self.days.lineEdit().setAlignment(QtCore.Qt.AlignCenter)

        self.byTimeButton = QtWidgets.QPushButton()
        self.byTimeButton.setGeometry(QtCore.QRect(10, 10, 201, 61))
        font = QtGui.QFont()
        font.setFamily("Gisha")
        font.setPointSize(28)
        self.byTimeButton.setFont(font)
        self.byTimeButton.setObjectName("byTimeButton")

        layoutOfOptions = QHBoxLayout()
        layoutOfOptions.addWidget(self.timeEdit)
        layoutOfOptions.addWidget(self.days)
        layoutOfOptions.addWidget(self.byTimeButton)
        widget1 = QWidget()
        widget1.setLayout(layoutOfOptions)
        self.vbox.addWidget(widget1)

        self.label = QtWidgets.QLabel()
        self.label.setGeometry(QtCore.QRect(0, 150, 300, 8000))
        font = QtGui.QFont()
        font.setPointSize(24)
        font.setFamily("Gisha")
        self.label.setFont(font)
        self.label.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.label.setAlignment(QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)
        self.label.setObjectName("label")
        self.vbox.addWidget(self.label)

    def update_current_time(self):
        from PyQt5.QtCore import QTime
        time = QTime(int(get_now()[1].split(":")[0]), int(get_now()[1].split(":")[1]))
        self.timeEdit.setTime(time)
        self.days.addItems(list("אבגדהו"))
        self.days.setCurrentText(get_now()[0])

    def add_events_to_buttons(self):
        self.nowButton.clicked.connect(self.show_now)
        self.showInfoButton.clicked.connect(self.showInfo)
        self.showTeacherButton.clicked.connect(self.showTeacher)
        self.showClassesButton.clicked.connect(self.showClasses)
        self.showCoursesButton.clicked.connect(self.showCourses)
        self.byTimeButton.clicked.connect(self.showByTime)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.nowButton.setText(_translate("MainWindow", "חדרים פנויים עכשיו"))
        self.showInfoButton.setText(_translate("MainWindow", "הצג מידע"))
        self.showTeacherButton.setText(_translate("MainWindow", "הצג על פי המרצים"))
        self.showClassesButton.setText(_translate("MainWindow", "הצג על פי כיתות"))
        self.showCoursesButton.setText(_translate("MainWindow", "הצג על פי הקורסים"))
        self.byTimeButton.setText(_translate("MainWindow", "הצג ע\"פ זמן"))
        self.label.setOpenExternalLinks(True)

        self.label.setText("""<a href=\"http://bit.ly/availableRoomsBot\">
        היי וברוך הבא לתוכנה של מציאת חדרים פנויים, 
        <br>
          ועוד מלא דברים נחמדים 😇
        <br>
        התוכנה הזו היא גרסה נייחת ואופליין של הבוט - @availableRoomsBot 🤖
        <br>
         מוזמן ללחוץ על הטקסט ולבדוק האם יש עדכונים 
         <br>
         http://bit.ly/availableRoomsBot
        <br><br>
        העדכון האחרון של התוכנה הזו היא בי' בטבת תש"פ
        </a>""")

    def showTeacher(self):
        self.comboBox.clear()
        self.comboBox.clearFocus()
        self.comboBox.addItems(self.d.teachers)
        self.showInfoButton.setEnabled(True)

    def showCourses(self):
        self.comboBox.clear()
        self.comboBox.clearFocus()
        self.comboBox.addItems(self.d.subjects)
        self.showInfoButton.setEnabled(True)

    def setMessage(self, text):
        self.label.setText(text)

    def showByTime(self):
        time = self.timeEdit.text()
        day = self.days.currentText()
        if (day in "אבגדהוז"):
            value = day + " " + time
            text = self.d.answer_to_message(value)
            self.setMessage(text)

    def showClasses(self):
        self.comboBox.clear()
        self.comboBox.clearFocus()
        self.comboBox.addItems(map(lambda i: i[0] + " " + str(i[1]), self.d.classes))
        self.showInfoButton.setEnabled(True)

    def show_now(self):
        text = self.d.get_class_for_now()
        self.setMessage(text)

    def showInfo(self):
        value = self.comboBox.currentText()
        text = self.d.answer_to_message(value)
        self.setMessage(text)


def main():
    app = QtWidgets.QApplication(argv)
    main = MainWindow()
    exit(app.exec_())


if __name__ == '__main__':
    main()
