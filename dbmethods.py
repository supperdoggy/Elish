import random
import string

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
    i = 0
    try:
        while True:
            if items.query[i].name == name and items.query[i].price == price and items.query[i].category == category:
                return items.query[i]
            else:
                i += 1
    except:
        return 404

# appending item to the basket
def appendToBasket(name, price, category, basket, current_user, db):
    if itemIsInBasketAlready(name, price, category, basket, current_user):
        item = getItemFromBasket(name, price, category, basket, owner)
        item.howMany += 1
        db.session.commit()
    else:
        newBasketItem = basket(name=name, price=price, category=category, owner=current_user)
        db.session.add(newBasketItem)
        db.session.commit()
    return 0

# getting item from the basket
def getItemFromBasket(name, price, category, basket, owner):
    i = 0
    try:
        while True:
            if basket.query[i].name == name and basket.query[i].price == price and basket.query[i].category == category and basket.query[i].owner == owner:
                return basket.query[i]
            else:
                i += 1
    except:
        return 404

# checking username and password
def checkAccess(password, username, users):
    i = 0
    try:
        while True:
            if users.query[i].username == username and users.query[i].password == password:
                return True
            else:
                i += 1
    except:
        return False

# checking if item exists in db
def checkIfExists(name, price, category, items):
    i = 0
    try:
        while True:
            if items.query[i].name == name and items.query[i].price == price and items.query[i].category == category:
                return True
            else:
                i += 1
    except:
        return False

# getting Total value of the basket
def getTotal(basket):
    total = 0
    for n in basket:
        total += n.price * n.howMany
    return total

# deleting everything from basket
def deleteAllBasket(basket, db):
    for n in basket:
        db.session.delete(n)
        db.session.commit()
            