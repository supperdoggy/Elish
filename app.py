from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from dbmethods import *
from flask_migrate import Migrate
from flask import session
from sqlalchemy.orm import sessionmaker
from save import *
from constants import *

# TODO: possibility of adding new masters and removing old one
# TODO: short, long cut
# TODO: make it possible to write amout of paint

# TODO: SIMPLOFY CODE
#       maybe make own methods for app.route?

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


# ========================== DATABASE MODELS ========================== #

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
    # masterName = db.Column(db.String)
    howMany = db.Column(db.Integer, default=1)

    def __repl__(self):
        return "<Item %s>" % self.id

# ========================== DATABASE MODELS ========================== #

# ==================================================== TEMPLATES ==================================================== #


# ========================== MAIN INDEX ========================== #

# path with items which are in selected category
@app.route("/<category>")
def main(category):
    if session.get("logged_in"):
        # test current user
        current_user = session.get("user")

        # if category = 0 then we just getting all items, else getting items which in selected category
        if category == 0:
            allItems = items.query.all()
        else:
            allItems = items.query.filter_by(category=category).all()

        # getting all items in basket
        itemsInBasket = basket.query.filter_by(owner=current_user).all()

        # getting basket price
        total = getTotal(itemsInBasket)

        # checks if basket is empty by value of total
        empty = False if total != 0 else True

        # rendering template
        return render_template("index.html", items=allItems, basket=itemsInBasket, total=total, empty=empty, categories=categories)
    else:
        return redirect("/login")

# path for main index
@app.route("/")
def mainIndex():
    return main(0)
# тут кнопочки для того шоб вибрати послугами
# також корзина з вибраними послугами

# ========================== MAIN INDEX ========================== #

# ========================== BILL TEMPLATE ========================== #
@app.route("/bill")
def bill():
    if session.get("logged_in"):
        current_user = session.get("user")
        itemsInBasket = basket.query.filter_by(owner=current_user).all()
        total = getTotal(itemsInBasket)
        return render_template("bill.html", basket=itemsInBasket, total=total, master=session.get("master"))
    else:
        return redirect("/login")

# ========================== BILL TEMPLATE ========================== #

# ========================== LOGIN ========================== #
@app.route("/login", methods=["POST", "GET"])
def login():
    # resseting cookies
    session["logged_in"] = False
    session["user"] = None
    # TODO: add master for each category and more checks as well
    session["master"] = None

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
# ========================== LOGIN ========================== #

# ==================================================== TEMPLATES ==================================================== #

# ==================================================== ACTION URLS ==================================================== #


# path for adding item to basket
@app.route("/addItemToBasket/<name>/<int:price>/<category>")  # /<masterName>
def addItemToBasket(name, price, category):  # masterName
    if session.get("logged_in"):
        current_user = session.get("user")
        if itemIsInBasketAlready(name, price, category, basket, current_user):
            item = getItemFromBasket(
                name, price, category, basket, current_user)
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

        # checking if item is in the basket already
        # if is and amout is more  than 1 than it deletes only one piece from howMuch
        if itemIsInBasketAlready(name, price, category, basket, current_user) and getItemFromBasket(name, price, category, basket, current_user).howMany > 1:
            getItemFromBasket(name, price, category, basket,
                              current_user).howMany -= 1

        # if not then it deletes the whole item from the basket
        else:
            db.session.delete(getItemFromBasket(
                name, price, category, basket, current_user))

        db.session.commit()
        # saving changes of db
        # redirecting into main index
        return redirect("/")
    else:
        return redirect("/login")

# path for saving data
@app.route("/checkout")
def checkout():
    if session.get("logged_in"):
        current_user = session.get("user")

        # JUST TEST MASTER PICK !
        master = session.get("master")
        # NEED TO CHOOSE ONE MASTER PER CATEGORY IN BASKET !

        # getting items in current_user`s basket
        itemsInBasket = basket.query.filter_by(owner=current_user).all()

        # getting total price of items in basket
        total = getTotal(itemsInBasket)

        # saving data into txt file named after today`s date
        saveData(itemsInBasket, total, current_user, master)

        # deleting items in basket
        deleteAllModel(itemsInBasket, db)

        # deleting master name
        session["master"] = None

        # redirecting to main index
        return redirect("/")
    else:
        return redirect("/login")

# ====================================================
#                    DANGER ZONE                     #
# ====================================================

# TODO: for each category found in basket pick master
@app.route("/master", methods=["POST", "GET"])
def chooseMaster():
    if session.get("logged_in"):
        if request.method == "POST":
            session["master"] = request.form["selector"]
            return redirect("/bill")
        else:
            return render_template("master.html", masters=masters)
    else:
        return redirect("/login")

# ====================================================
#                    DANGER ZONE                     #
# ====================================================

# ==================================================== ACTION URLS ==================================================== #


if __name__ == "__main__":
    app.run(debug=True)
