import telebot
from constants import token, MaksId

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

bot.polling(none_stop=True)

