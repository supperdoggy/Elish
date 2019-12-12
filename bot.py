import telebot
from constants import token, MaksId
import datetime

bot = telebot.TeleBot(token)

@bot.message_handler(commands=["start"])
def greetings(message):
    if message.from_user.id == MaksId:
        bot.reply_to(message, "Дарова макс")
    else:
        bot.reply_to(message, "Привіт, адміністраторе")

    main = telebot.types.ReplyKeyboardMarkup(row_width=3)
    btn1 = telebot.types.KeyboardButton("Отримати виручку на даний момент")
    btn2 = telebot.types.KeyboardButton("Отримати виручку за конкретну дату")
    main.add(btn1, btn2)
    bot.send_message(message.from_user.id, "Виберіть доступну опцію", reply_markup=main)

    print(message)

@bot.message_handler(content_types=["text"])
def answer(message):
    if message.text == "Отримати виручку на даний момент":
        try:
            f = open("bills/" + str(datetime.date.today()) + ".txt", "rb")
            bot.send_document(message.from_user.id, f)
            bot.reply_to(message, "Ось виручка за сьогоднішній день")
            f.close()
        except:
            bot.reply_to(message, "За сьогодні виручки немає")

    elif message.text == "Отримати виручку за конкретну дату":
        bot.reply_to(message, "Увведіть дату у форматі рік-місяць-день щоб отримати звіт за конкретний день\nприклад: 2019-12-12")

    elif message.text[0] == "2":
        try:
            f = open("bills/" + message.text + ".txt", "rb")
            bot.send_document(message.from_user.id, f)
            bot.reply_to(message, "Ось звіт за даний день")
            f.close()
        except:
            bot.reply_to(message, "Не вдалося знайти звіт за даний день")
    
    else:
        bot.reply_to(message, "Я не розумію що ви написали")

bot.polling(none_stop=True)

