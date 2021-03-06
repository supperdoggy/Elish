import random
import string
from save import saveData

# checking if item is in the basket
def itemIsInBasketAlready(name, price, category, basket, current_user):
    if getItemFromBasket(name, price, category, basket, current_user) != 404:
        return True
    else:
        return False

# generating random string
def randomString(stringLenght=24):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(stringLenght))

# getting item from items
def getItemFromItems(name, price, category, items):
    itemsFromItems = items.query.all()
    for n in itemsFromItems:
        if name == n.name and price == n.price and category == n.category:
            return n
    return 404

# appending item to the basket
def appendToBasket(name, price, category, basket, current_user, db):
    if itemIsInBasketAlready(name, price, category, basket, current_user):
        # changed here from owner to current_user, check if it works
        item = getItemFromBasket(name, price, category, basket, current_user)
        item.howMany += 1
        db.session.commit()
    else:
        newBasketItem = basket(name=name, price=price, category=category, owner=current_user)
        db.session.add(newBasketItem)
        db.session.commit()

# getting item from the basket
def getItemFromBasket(name, price, category, basket, owner):
    itemsInBasket = basket.query.filter_by(owner=owner).all()
    for n in itemsInBasket:
        if name == n.name and price == n.price and category == n.category:
            return n
    return 404

# checking username and password
def checkAccess(password, username, users):
    i = 0
    usersList = users.query.all()
    for user in usersList:
        if username == user.username and password == user.password:
            return True
    return False

# checking if item exists in db
def checkIfExists(name, price, category, model):
    i = 0
    itemsInModel = model.query.all()
    for n in itemsInModel:
        if name == n.name and price == n.price and category == n.category:
            return True
    return False

# getting Total value of the basket
def getTotal(basket):
    total = 0
    for n in basket:
        total += n.price * n.howMany
    return total

# deleting everything from db model
def deleteAllModel(model, db):
    for n in model:
        db.session.delete(n)
        db.session.commit()

# checks which categories are in basket and returns it via list
def getCategories(basket, owner):
    items = basket.query.filter_by(owner=owner).all()
    categories = []
    for i in items:
        if i.category not in categories:
            categories.append(i.category)
    return categories

def checkout(session, basket, db):
    # getting current user
    current_user = session.get("user")
    # getting list with masters and categories
    masters = session.get("masters")

    # getting items in current_user`s basket
    itemsInBasket = basket.query.filter_by(owner=current_user).all()

    # getting total price of items in basket
    total = getTotal(itemsInBasket)

    # saving data into txt file named after today`s date
    saveData(itemsInBasket, total, current_user, masters)

    # deleting items in basket
    deleteAllModel(itemsInBasket, db)

    # deleting masters names
    session["masters"] = None
