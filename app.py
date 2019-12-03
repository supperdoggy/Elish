from flask import Flask, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from dbmethods import *
from flask_migrate import Migrate

# TODO: fill db with items

# pls ignore syntax errors in db (ide bug)

# declaring app and template folder
app = Flask(__name__, template_folder="templates")
# configurating db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
# getting db
db = SQLAlchemy(app)
# creating migration settings
migrate = Migrate(app, db)

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
    name = db.Column(db.String
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
    # test current user
    current_user = "admin"
    # getting all items
    allItems = items.query.get_or_404().all()
    # TODO: create login
    # getting all items in basket
    itemsInBasket = basket.query.filter_by(owner=current_user).all()
    # rendering template
    return render_template("index.html", allItems=allItems, itemsInBasket=itemsInBasket)

# тут будуть кнопочки для того шоб вибрати послугами
# також буде корзина з вибраними послугами

# path for adding item to basket
@app.route("/addItemToBasket/<name>/<price>/category")
def addItemToBasket(name, price, category):
    # getting item which we want to add into basket
    item = getItemFromItems(name, price, category, items)
    # appending item into basket
    appendToBasket(item, basket, current_user, db)
    # redirecting into main index
    return redirect("/")

# path for adding item into db
@app.route("/additemIntoItems/<name>/<price>/<category>")
def additemIntoItems(name, price, category):
    # creating model of item
    newItem = items(name=name, price=price, category=category)
    # appending into db
    db.session.add(newItem)
    # saving changes of db
    db.session.commit()
    # redirecting into main index
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

@app.route("/deleteitemfrombasket/<name>/<price>/<category>")
def deleteItemFromBasket(name, price, category):
    # getting item from basket
    item = getItemFromBasket(name, price, category, basket, "admin") # current user
    # deleting item from db
    db.session.delete(item)
    # saving changes of db
    db.session.commit()
    # redirecting into main index
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True)