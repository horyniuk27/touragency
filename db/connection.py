from pymongo import MongoClient

def getDatabase():
    """
    Підключення до MongoDB
    @return: db об'єкт для роботи з колекціями
    """
    client = MongoClient("mongodb://localhost:27017/")
    db = client["TourAgency"]
    return db
