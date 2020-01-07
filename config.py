# -*- coding: utf-8 -*-
import pytz
IST = pytz.timezone('Etc/GMT-2')
COMPUTER_LABS_FILE = "computer_labs"
FILEPATH_OF_DATA = "courses.csv"
filepathTal = "coursesTal.csv"
REPORT_FILE = "דיווח.csv"
context = ["id", "course name", "course code", "teacher", "day",
           "start time", "end time", "building", "room number", "type", "students number", "notes"]
API_CODE_OF_BOT = '-------------'

ADMIN_ID = 1

# Constants - for messages:
WELCOME_MESSAGE = """ברוך הבא! בחר אופציה מהתפריט ⬇😎"""

COMMAND_EMPTY_ROOM_NOW = 'חדרים פנויים עכשיו ⏳'
RESULT_RETURN = "אוקיי, חזרתי!"
COMMAND_BY_HOUR = 'לפי זמן ספיציפי ⏰'
RESULT_FOR_BY_HOUR = """אחלה,
שלח יום ושעה בפורמט של '<יום> HH:MM'
לדוגמה - א 15:15
"""

COMMAND_BY_ROOM = 'מידע על חדר 🏠'
RESULT_BY_ROOM = "בחר חדר מהרשימה, או הקלד בניין ומספר ⬇"

COMMAND_BY_TEACHER = 'מידע לפי מרצה 👨‍🏫'
RESULT_BY_TEACHER = "בחר מרצה מהרשימה, או הקלד את השם המלא במדוייק ⬇"

COMMAND_BY_SUBJECT = 'מידע לפי קורס 🎓'
RESULT_BY_SUBJECT = "בחר קורס מהרשימה, או הקלד את השם המלא במדוייק ⬇"

COMMAND_RETURN = "חזור 🔙"
COMMAND_FINDED_MISTAKE = "רעיון לשיפור? 🔎 רוצה לפרגן? 🤗 מצאת טעות? 😟"
COMMAND_ABOUT = "אודות הבוט 🤖"
RESULT_ABOUT = """הבוט נכתב במהלך חבורתא בסיבוכיות 🙈 ע"י @eitanttt.

הקוד כתוב בפייתון, רוצה לקבל אותו? 💻 בשמחה! דבר איתי. (חינם אין כסף, כמובן)"""
RESULT_MISTAKE = """רעיון לשיפור? 🔎 רוצה לפרגן? 🤗 איזה כיף😃 אתה יכול לכתוב כאן!

מצאת טעות במערכת? 😟 מתנצל על עוגמת הנפש, טעות לעולם חוזר וכו'...
הנתונים נלקחים מהלב נט, ויש פעמים שהם לא הכי מעודכנים בעולם 😔
אבל אל דאגה! יחד אנחנו נבנה מאגר טוב יותר ומעודכן יותר! 💪
אנא כתוב לי - במילים חופשיות - על הטעות שמצאת.
ובעז"ה אני אעבור על זה ואתקן 😇
תודה!"""

COMMAND_SENED_MISTAKE = "קיבלתי, תודה!😁"
# end constants - for messages
