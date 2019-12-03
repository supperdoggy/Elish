import random
import string


def randomString(stringLenght=24):
    return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(stringLenght))

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

def appendToBasket(name, price, category, basket, current_user, db):
    newBasketItem = basket(name=name, price=price, category=category, owner=current_user)
    db.session.add(newBasketItem)
    db.session.commit()
    return 0

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

def getTotal(basket):
    i = 0
    prices = []
    while True:
        try:
            if basket.query[i].price.__contains__("-"):
                j = -1
                while True:
                    if basket.query[i].price != "-" or basket.query[i].price == "-":
                        basket.query[i].price.remove(basket.query[i].price[j])
                        j -= 1
                    else:
                        break
                    prices.append(basket.query[i].price)
                    print(prices)
            else:
                prices.append(basket.query[i].price)
        except:
            return prices
        
            