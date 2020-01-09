import datetime
import os

# saving data for python bot
def saveData(basket, total, current_user, masters):
    if os.path.exists("bills/" + str(datetime.date.today()) + ".txt"):
        f = open("bills/" + str(datetime.date.today()) + ".txt", "a+")
        
    else:
        f = open("bills/" + str(datetime.date.today()) + ".txt", "w+")

    f.write("\n"+"-"*10 + "\n")
    f.write("Касир: %s" %current_user + "\n")
    f.write("Час: %s"%datetime.datetime.now() + "\n\n")

    for m in masters:
        f.write(m + "\n")

    for n in basket:
        f.write("Ім'я послуги: " + str(n.name) + "\n")
        f.write("Кількість: " + str(n.howMany) + "\n")
        f.write("Ціна за послугу: " + str(n.price) + "\n")
        f.write("Всього ціна: " + str(n.price * n.howMany) + "\n")
        f.write("\n")
    f.write("\n\n")
    f.write("Вартість послуг: " + str(total) + "\n")
    f.close()