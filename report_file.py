from config import *
import csv
CHANNEL_ID = -1001246033663

def get_file_by_req(update, context):
    message = update.message.text
    if update.message.from_user['username'] != 'eitanttt':
        return False
    if len(message.split(" ")) == 2 and message.split(" ")[0] == "send" :
        f = open(REPORT_FILE, "r")
        if len(message.split(" ")) == 2 and message.split(" ")[1].isdigit():
            result = "\n".join(f.readlines()[-int(message.split(" ")[1]):])
        else:
            result = f.read()
        f.close()
        return result
    elif len(message.split(" ")) > 2 and message.split(" ")[0] == "send" and message.split(" ")[1].isdigit():
        user_id = int(message.split(" ")[1])
        new_message = " ".join(message.split(" ")[2:])
        context.bot.send_message(user_id, new_message)
        return "נשלח 👍"
    return False


def report_to_file(context, *row):
    message = "לב:\n" + "\n".join(map(lambda i: str(i), row))
    context.bot.send_message(CHANNEL_ID, str(message))
    with open(REPORT_FILE, 'a') as f:
        writer = csv.writer(f)
        writer.writerow(row)