from constants import categories, ukrLetters
from string import ascii_lowercase, digits
import json
import telebot

# shitcode, if text recieved fits the form: "str-int-category" 
# then returns list tuple with answer if fits, then returns values
# else just returns answer : False
def checkRequirements(text):
    i = 0
    firstChar = False
    minus = 0
    nums = ""
    category = "None"
    indexOfSecondMinus = -1
    while i < len(text):
        if text[i] != "-":
            firstChar = True
        if text[i] == "-" and minus == 1:
            minus += 1
            if i != (len(text)-1):
                indexOfSecondMinus = i+1
        elif text[i] == "-" and minus == 0:
            minus += 1
            indexOfFirstMinus = i
            name = text[0:indexOfFirstMinus]
            text = text.lower()
            text = text.replace(" ", "")
        if minus == 1 and text[i] not in ascii_lowercase and text[i] in digits:
            nums += text[i]
        elif minus == 1 and text[i] in ascii_lowercase:
            nums = False
        i+=1

    for c in categories:
        if text[indexOfSecondMinus:] == c.lower():
            category = c 
            break

    if minus == 2 and firstChar == True and category != "None" and nums != "":
        return {"ifTrue":True, "name":name, "price":nums, "category":category}

    else:
        return {"ifTrue":False}

# saving data into buffer folder
def saveData(data, userID):
    f = open("buffer/%s.json" %userID, "w+")
    json.dump(data, f)

# getting data from buffer folder
def getData(userID):
    try:
        f = open("buffer/%s.json" %userID, "r")
        return json.load(f)
    except:
        return None

# starter keyboard which comes right after /start command
def sendStarterKeyboard(bot, message):
    # keyboard
    main = telebot.types.ReplyKeyboardMarkup(row_width=3)
    btn1 = telebot.types.KeyboardButton("Отримати виручку на даний момент")
    btn2 = telebot.types.KeyboardButton("Отримати виручку за конкретну дату")
    btn3 = telebot.types.KeyboardButton("Додати нову послугу")
    main.add(btn1, btn2, btn3)
    bot.send_message(message.from_user.id, "Виберіть доступну опцію", reply_markup=main)