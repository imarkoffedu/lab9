import pymongo
from bson.objectid import ObjectId
import datetime

    

# Підключення до сервера MongoDB
client = pymongo.MongoClient("mongodb://localhost:27017/")

# Створення бази даних
db = client["sport_tracker"]

# Створення колекції (еквівалент таблиці в реляційних базах даних)
accounts = db["accounts"]
achievements = db["achievements"]
activities = db["activities"]

def find_user(query):
    user = accounts.find_one(query)
    if user:
        return user['_id']
    return False


def check_achievement(user_id, achievement_id):
    user = accounts.find_one({"_id": user_id})
    achievements = user.get('achievements')
    if achievements:
        for achievement in achievements:
            if achievement == achievement_id:
                return True
    return False


def trigger_achievements(user_id):
    activities = accounts.find_one({"_id": user_id}).get('activities')
    achievement1 = ObjectId('5f9f2c9b1c9d440000c4d39f')
    new_achievements = []
    if len(activities) >= 1 and check_achievement(user_id, achievement1) == False:
        accounts.update_one({"_id": user_id}, {"$push": {"achievements": achievement1}})
        new_achievements.append(achievement1)
        
    return new_achievements


def check_activity(activity):
    if activities.find_one({"type": activity}):
        return activity
    return False


def add_activity(user_id, activity, distance, time, date):
    if check_activity(activity):
        new_activity = {
            "activity": activity,
            "distance": distance,
            "time": time,
            "date": date
        }

        accounts.update_one({"_id": user_id}, {"$push": {"activities": new_activity}})

        new_achievements = trigger_achievements(user_id)

        return new_activity, new_achievements
    return False

# Додавання документів (еквівалент записів в таблиці)
account1 = {
    "name": "Oleksandr",
    "surname": "Lishchuk",
    "email": "tdshilugdfl@gmail.com",
    "password": "qwerty123",
    "reg_date": datetime.datetime.now()
}

account2 = {
    "name": "John",
    "surname": "Doe",
    "email": "luhdinbidgsgdufh@gmail.com",
    "password": "qwerty123",
    "reg_date": datetime.datetime.now()
}

# Вставка документів
inserted_data1 = accounts.insert_one(account1)
inserted_data2 = accounts.insert_one(account2)

# Зчитування документів
for document in accounts.find():
    print(document)

# Оновлення документа
user_1 = find_user({"name": "Vladyslav", "surname": "Hroshev"})
add_activity(user_1, "running", 1000, 1000, datetime.datetime.now())
add_activity(user_1, "cycling", 1000, 1000, datetime.datetime.now())

# Видалення документа
delete_query = {"name": "John", "surname": "Doe"}
accounts.delete_one(delete_query)

# Зчитування документів після оновлення та видалення
print("Після оновлення та видалення:")
for document in accounts.find():
    print(document)

# Закриття підключення
client.close()
