import telebot
from constants import token, MaksId
import datetime
from botmethods import *
import os
from app import db, items

# TODO: Fill db with items via telegram bot

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def greetings(message):
    if message.from_user.id == MaksId:
        bot.reply_to(message, "Дарова макс")
    else:
        bot.reply_to(message, "Привіт, адміністраторе")

    # sends starter keyboard
    sendStarterKeyboard(bot, message)

    print(message)

@bot.message_handler(content_types=["text"])
def answer(message):
    text = message.text
    if text == "Отримати виручку на даний момент":
        try:
            f = open("bills/" + str(datetime.date.today()) + ".txt", "rb")
            bot.send_document(message.from_user.id, f)
            bot.reply_to(message, "Ось виручка за сьогоднішній день")
            f.close()
        except:
            bot.reply_to(message, "За сьогодні виручки немає")

    elif text == "Отримати виручку за конкретну дату":
        bot.reply_to(message, "Увведіть дату у форматі рік-місяць-день щоб отримати звіт за конкретний день\nприклад: 2019-12-12")

    elif text == "Додати нову послугу":
        bot.reply_to(message, "Уведіть назву в форматі товар-ціна-Категорія\nНаприклад: 'Стрижка жіноча-12-Стрижка'")

    # answer
    elif text == "Так":
        data = getData(message.from_user.id)

        # adding item
        newItem = items(name=data["name"], price=data["price"], category=data["category"])

        db.session.add(newItem)
        db.session.commit()

        # adding item

        sendStarterKeyboard(bot, message)
        os.remove("buffer/%s.json" % message.from_user.id)
    elif text == "Ні":
        try:
            os.remove("buffer/%s.json" % message.from_user.id)
            bot.reply_to(message, "Готово")
            sendStarterKeyboard(bot, message)
        except:
            bot.reply_to(message, "Помилка")
            sendStarterKeyboard(bot, message)

    elif text[0] == "2":
        try:
            f = open("bills/" + message.text + ".txt", "rb")
            bot.send_document(message.from_user.id, f)
            bot.reply_to(message, "Ось звіт за даний день")
            f.close()
        except:
            bot.reply_to(message, "Не вдалося знайти звіт за даний день")

    elif text[0].lower() in ascii_lowercase or text[0].lower() in ukrLetters:
        if checkRequirements(message.text)["ifTrue"]:
            data = checkRequirements(message.text)
            ans = "Ім'я послуги - " + data["name"] + "\n" + "Ціна послуги - " + data["price"] + "\n"+ "Категорія послуги - " + data["category"]
        else:
            ans = "NO"
        bot.send_message(message.chat.id, ans)

        # keyboard
        main = telebot.types.ReplyKeyboardMarkup(row_width=3)
        btn1 = telebot.types.KeyboardButton("Так")
        btn2 = telebot.types.KeyboardButton("Ні")

        saveData(data, message.from_user.id)

        main.add(btn1, btn2)
        bot.send_message(message.chat.id, "Ви дійсно хочете додати в базу цей продукт?", reply_markup=main)

    


bot.polling(none_stop=True)

