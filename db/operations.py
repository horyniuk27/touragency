from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient("mongodb://localhost:27017/")
db = client["touristDB"]

# --------- Users --------- #
def addUser(login, password, role):
    if db.users.find_one({"login": login}):
        return False
    db.users.insert_one({"login": login, "password": password, "role": role})
    return True

def getUser(login):
    return db.users.find_one({"login": login})

# --------- Tourists --------- #
def addTourist(data):
    db.tourists.insert_one(data)

def getAllTourists():
    return list(db.tourists.find())

def deleteTourist(touristId):
    db.tourists.delete_one({"_id": ObjectId(touristId)})

def updateTourist(touristId, data):
    db.tourists.update_one({"_id": ObjectId(touristId)}, {"$set": data})

# --------- Hotels --------- #
def addHotel(data):
    db.hotels.insert_one(data)

def getAllHotels():
    return list(db.hotels.find())

# --------- Excursions --------- #
def addExcursion(data):
    db.excursions.insert_one(data)

def getAllExcursions():
    return list(db.excursions.find())

# --------- Cargo --------- #
def addCargo(data):
    db.cargo.insert_one(data)

def getCargoByTourist(touristName):
    return list(db.cargo.find({"tourist": touristName}))
