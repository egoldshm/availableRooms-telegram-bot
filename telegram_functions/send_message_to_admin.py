from config import ADMIN_ID


def send_to_admin(update, context):
    user = update.message.from_user
    result = """
    הודעה חדשה 📢
    מזהה: {}
    שם: {} 
    שם אחרון: {}
    שם משתמש: {}
     
     
     {}""".format(user.id, user.first_name, user.last_name, user.username, update.message.text)
    context.bot.send_message(ADMIN_ID, result)