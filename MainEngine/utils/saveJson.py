import json
from datetime import datetime, timedelta

def saveJson(error):
    with open("errorLogs.json","r+") as file:
        dateNow = datetime.now().strftime("%Y/%m/%d")
        errors = json.load(file)
        saveError = f"{dateNow} - {error}"
        if saveError not in errors['error']:
            errors['error'].append(saveError)
        file.seek(0)
        json.dump(errors, file, indent = 4)

def saveRem(rem):
    with open("MainEngine//Database//remember.json","r+") as file:
        dateNow = datetime.now().strftime("%Y/%m/%d")
        reminder = json.load(file)
        if dateNow not in reminder.keys():
            reminder[dateNow] = []
        reminder[dateNow].append(rem)
        file.seek(0)
        json.dump(reminder, file, indent = 4)

def readRem(filter):
    with open("MainEngine//Database//remember.json","r+") as file:
        yesterday = (datetime.now()+timedelta(1)).strftime("%Y/%m/%d")
        today = datetime.now().strftime("%Y/%m/%d")
        tomorrow = (datetime.now()-timedelta(1)).strftime("%Y/%m/%d")
        filterDict = {"today":today,"yesterday":yesterday,"tomorrow":tomorrow}
        reminder = json.load(file)
        if filter in filterDict.keys():
            return reminder[filterDict[filter]]
        if reminder[today]:
            return reminder[today]
        else:
            return f"You are all caught up boss. No any reminders left"