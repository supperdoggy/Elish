from flask import Flask, redirect, render_template,request
from flask_sqlalchemy import SQLAlchemy
import datetime
from dbmethods import *
from flask_migrate import Migrate
from flask  import  session
from sqlalchemy.orm import sessionmaker
from save import *
from constants import *


# declaring app and template folder
app = Flask(__name__, template_folder="templates")
# configurating db
app.config['SQLALCHEMY_DATABASE_URI'] = dbPath
# getting db
db = SQLAlchemy(app)
# creating migration settings
migrate = Migrate(app, db)
# secret key
app.secret_key = secretKey

# ============================================= db models =============================================

# model class for users
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniqueId = db.Column(db.String, default=randomString())
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())

    def __repl__(self):
        return "<User %s>" % self.id

# model class for items
class items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniqueId = db.Column(db.String(24))
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    category = db.Column(db.String(20))

    def __repl__(self):
        return "<Item %s>" % self.id

# model class for basket
class basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    date_created = db.Column(db.DateTime, default=datetime.datetime.now())
    category = db.Column(db.String(20))
    owner = db.Column(db.String)
    howMany = db.Column(db.Integer, default=1)

    def __repl__(self):
        return "<Item %s>" % self.id

# ============================================= db models =============================================

# path for main index
@app.route("/")
def mainIndex():
    if session.get("logged_in"):
        # test current user
        current_user = session.get("user")

        # getting all items
        allItems = items.query.all()

        # getting all items in basket
        itemsInBasket = basket.query.filter_by(owner=current_user).all()
        
        # getting basket price
        total = getTotal(itemsInBasket)


        # TODO: filter items by category


        # checks if basket is empty by value of total
        empty = False if total != 0 else True

        # rendering template
        return render_template("index.html", items=allItems, basket=itemsInBasket,total=total, empty=empty)
    else:
        return redirect("/login")
# тут кнопочки для того шоб вибрати послугами
# також корзина з вибраними послугами

# path for adding item to basket
@app.route("/addItemToBasket/<name>/<int:price>/<category>")
def addItemToBasket(name, price, category):
    if session.get("logged_in"):
        current_user = session.get("user")
        if itemIsInBasketAlready(name, price, category, basket, current_user):
            item = getItemFromBasket(name, price, category, basket, current_user)
            item.howMany += 1
        else:
            appendToBasket(name, price, category, basket, current_user, db)

        db.session.commit()
        return redirect("/")
    else:
        return redirect("/login")

# path for adding item into db
@app.route("/additemIntoItems/<name>/<int:price>/<category>")
def additemIntoItems(name, price, category):
    if session.get("logged_in"):
        # creating model of item
        newItem = items(name=name, price=price, category=category)
        # appending into db
        db.session.add(newItem)
        # saving changes of db
        db.session.commit()
        # redirecting into main index
        return redirect("/")
    else:
        return redirect("/")

# path for deleting item from item model
@app.route("/deleteitemFromItems/<name>/<int:price>/<category>")
def deleteitemFromItems(name, price, category):
    # getting item
    item = getItemFromItems(name, price, category, items)
    # deleting item from db
    db.session.delete(item)
    # saving changes of db
    db.session.commit()
    # redirecting into main index
    return redirect("/")

# path from deleting item from basket
@app.route("/deleteitemfrombasket/<name>/<int:price>/<category>")
def deleteItemFromBasket(name, price, category):
    if session.get("logged_in"):
        current_user = session.get("user")
        # getting item from basket
        # deleting item from db
        
        # кароче треба замість того шоб добавляти одне й те саме, можна просто приробити віконечко і там відображати кількість товарів
        # + можна буде зробити розрахунок на фарбу лол
        # але тоді треба буде тупо додати всі товари

        # TODO: rewrite this if else statement cus this is shit
        if itemIsInBasketAlready(name, price, category, basket, current_user) and getItemFromBasket(name, price, category, basket, current_user).howMany > 1:
            getItemFromBasket(name, price, category, basket, current_user).howMany -= 1
            db.session.commit()
        else:
            db.session.delete(getItemFromBasket(name, price, category, basket, current_user))
            db.session.commit()
        # saving changes of db
        # redirecting into main index
        return redirect("/")
    else:
        return redirect("/login")


@app.route("/checkout")
def checkout():
    if session.get("logged_in"):
        current_user = session.get("user")
        itemsInBasket = basket.query.filter_by(owner=current_user).all()
        
        # saving data into txt file named after todays date
        total = getTotal(itemsInBasket)
        saveData(itemsInBasket, total)

        # deleting items in basket
        deleteAllBasket(itemsInBasket, db)

        return redirect("/")
    else:
        return redirect("/login")

# bill template
@app.route("/bill")
def bill():
    if session.get("logged_in"):
        current_user = session.get("user")
        itemsInBasket = basket.query.filter_by(owner=current_user).all()
        total = getTotal(itemsInBasket)
        return render_template("bill.html", basket=itemsInBasket, total=total)
    else:
        return redirect("/login")

# ========================== login ========================== #
@app.route("/login", methods=["POST", "GET"])
def login():
    # resseting cookies
    session["logged_in"] = False
    session["user"] = None

    if request.method == "POST":
        # if password and username matches in db then True
        if checkAccess(request.form["password"], request.form["username"], users):

            # updating cookie
            session["logged_in"] = True
            session["user"] = request.form["username"]

            return redirect("/")
        else:
            # else redirect back to login
            return redirect("/login")
    else:
        return render_template("login.html")
# ========================== login ========================== #

if __name__ == "__main__":
    app.run(debug=True)