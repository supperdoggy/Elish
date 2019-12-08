from flask import Flask, redirect, render_template,request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dbmethods import *
from flask_migrate import Migrate
from flask  import  session
from sqlalchemy.orm import sessionmaker

# TODO: fix total basket value and checkout

# declaring app and template folder
app = Flask(__name__, template_folder="templates")
# configurating db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# getting db
db = SQLAlchemy(app)
# creating migration settings
migrate = Migrate(app, db)
# secret key
app.secret_key = "dsagfhjsagkhjrgu123hjkgerkfhjsaghfjgh3qj1gwqruyaf"

# model class for users
class users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniqueId = db.Column(db.String, default=randomString())
    username = db.Column(db.String(200), unique=True)
    password = db.Column(db.String(200))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repl__(self):
        return "<User %s>" % self.id

# model class for items
class items(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    uniqueId = db.Column(db.String(24))
    name = db.Column(db.String)
    price = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(20))

    def __repl__(self):
        return "<Item %s>" % self.id

# model class for basket
class basket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.String(20))
    owner = db.Column(db.String)

    def __repl__(self):
        return "<Item %s>" % self.id

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

        # doesnt work total
        total = getTotal(itemsInBasket)
        # TODO: filter items by category

        # rendering template
        return render_template("index.html", items=allItems, basket=itemsInBasket,total=total)
    else:
        return redirect("/login")
# тут будуть кнопочки для того шоб вибрати послугами
# також буде корзина з вибраними послугами

# path for adding item to basket
@app.route("/addItemToBasket/<name>/<price>/<category>")
def addItemToBasket(name, price, category):
    if session.get("logged_in"):
        # test current user
        current_user = session.get("user")
        # checking if items exists
        if checkIfExists(name, price, category, items):
        # appending item into basket
            appendToBasket(name, price, category, basket, current_user, db)
        # redirecting into main index
        return redirect("/")
    else:
        return redirect("/login")

# path for adding item into db
@app.route("/additemIntoItems/<name>/<price>/<category>")
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
@app.route("/deleteitemFromItems/<name>/<price>/<category>")
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
@app.route("/deleteitemfrombasket/<name>/<price>/<category>")
def deleteItemFromBasket(name, price, category):
    if session.get("logged_ in"):
        current_user = session.get("user")
        # getting item from basket
        item = getItemFromBasket(name, price, category, basket, current_user) # current user
        # deleting item from db
        db.session.delete(item)
        # saving changes of db
        db.session.commit()
        # redirecting into main index
        return redirect("/")
    else:
        return redirect("/login")

@app.route("/checkout")
def checkout():
    if session.get("logged_in"):
        current_user = session.get("user")
        itemsInBasket = basket.query.filter_by(owner=current_user).all()
        deleteAllBasket(itemsInBasket, db)
        return redirect("/")
    # checkouting 
    # deleting items from basket
    else:
        return redirect("/login")

@app.route("/login", methods=["POST", "GET"])
def login():
    session["logged_in"] = False
    session["user"] = None
    if request.method == "POST":
        if checkAccess(request.form["password"], request.form["username"], users):
            session["logged_in"] = True
            session["user"] = request.form["username"]
            return redirect("/")
        else:
            return redirect("/login")
    else:
        return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)