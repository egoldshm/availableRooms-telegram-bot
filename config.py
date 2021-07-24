# -*- coding: utf-8 -*-
import pytz
IST = pytz.timezone('Etc/GMT-2')
COMPUTER_LABS_FILE = "computer_labs"
FILEPATH_OF_DATA = "courses.csv"

STATISTICS_COURSES_FILE = ""

REPORT_FILE = "דיווח.csv"
context = ["id", "course name", "course code", "teacher", "day",
           "start time", "end time", "building", "room number", "type", "students number", "notes"]
API_CODE_OF_BOT = '1028809311:AAGr-JzIAGItdtpeX6WUAPquGdzlMmIyENE'
URL = "https://emptyclassrooms.herokuapp.com/"
ADMIN_ID = 114534171

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
RESULT_BY_ROOM = "בחר בניין מהרשימה, או הקלד בניין ומספר ⬇"
RESULT_BY_ROOM1 = "בחר חדר מהרשימה, או הקלד בניין ומספר ⬇"

COMMAND_BY_TEACHER = 'מידע לפי מרצה 👨‍🏫'
RESULT_BY_TEACHER = "בחר אות שבה מתחיל שם המשפחה של המרצה, או הקלד את השם המלא במדוייק ⬇"

COMMAND_BY_SUBJECT = 'מידע לפי קורס 🎓'
RESULT_BY_SUBJECT = "בחר אות שבה מתחיל שם קורס, או הקלד את השם המלא במדוייק ⬇"

RESULT_BY_LETTER = "בחר מהרשימה ⬇"

COMMAND_RETURN = "חזור 🔙"
COMMAND_FINDED_MISTAKE = "רעיון לשיפור? 🔎 רוצה לפרגן? 🤗 מצאת טעות? 😟"
COMMAND_ABOUT = "אודות הבוט 🤖"
RESULT_ABOUT = """הבוט נכתב בשביל הסטודנטים במרכז האקדמי לב ע"י @eitanttt מטעם אגודת הסטודנטים 😇

הקוד כתוב בפייתון, רוצה לקבל אותו? 💻 בשמחה! דבר איתי. (חינם אין כסף, כמובן)"""
RESULT_MISTAKE = """רעיון לשיפור? 🔎 רוצה לפרגן? 🤗 איזה כיף😃 אתה יכול לכתוב כאן!

מצאת טעות במערכת? 😟 מתנצל על עוגמת הנפש, טעות לעולם חוזר וכו'...
הנתונים נלקחים מהלב נט, ויש פעמים שהם לא הכי מעודכנים בעולם 😔
אבל אל דאגה! יחד אנחנו נבנה מאגר טוב יותר ומעודכן יותר! 💪
אנא כתוב לי - במילים חופשיות - על הטעות שמצאת.
ובעז"ה אני אעבור על זה ואתקן 😇
תודה!"""

COMMAND_SENED_MISTAKE = "קיבלתי, תודה!😁"
COMMAND_ONLY_COMPUTERS = "הצג מידע על מעבדות מחשבים בלבד 💻"
RESULT_ONLY_COMPUTERS = "קיבלתי, מעכשיו אציג לך מידע על מעבדות מחשבים בלבד 👍"
COMMAND_ALL_ROOMS = "הצג מידע על כל הכיתות במכון 🏠"
RESULT_ALL_ROOMS = "קיבלתי, מעכשיו אציג לך מידע על כל הכיתות במכון 👍"

COMMAND_AGUDA = "הבוט של האגודה ♥"
RESULT_AGUDA = "סטודנט במרכז האקדמי לב? ממש כדאי לך להיות רשום לבוט של אגודת הסטודנטים!🤗 אפשר למצוא שם המון מידע שימושי - ולקבל דרך שם את כל העדכונים של אגודת הסטודנטים! 🥳\n" \
               "\n\nמומלץ להצטרף!" \
               "@aguda_bot"
COMMAND_SHOW_ALL = "הראה הכל 🔍"
RESULT_SHOW_ALL = "מציג את כל התוצאות הרלוונטיות 👌"

HEB_LETTERS = "אבגדהוזחטיכלמנסעפצקרשת"
# end constants - for messages
