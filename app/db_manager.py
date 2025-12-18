from pymongo import MongoClient

def get_db_collection():
    client = MongoClient('mongo', 27017, username='user', password='password')
    db = client.school_db
    return db.students

def init_db():
    collection = get_db_collection()
    if collection.count_documents({}) == 0:
        data_seeds = [
            {"nombre": "Ana", "nota": 7, "localidad": "Madrid"},
            {"nombre": "Luis", "nota": 7, "localidad": "Barcelona"},
            {"nombre": "Marta", "nota": 5, "localidad": "Valencia"},
            {"nombre": "Juan", "nota": 9, "localidad": "Sevilla"},
            {"nombre": "Diego", "nota": 10, "localidad": "Bilbao"}
        ]
        collection.insert_many(data_seeds)

def add_student(nombre, localidad, nota):
    collection = get_db_collection()
    collection.insert_one({"nombre": nombre, "localidad": localidad, "nota": int(nota)})

def get_all_students():
    collection = get_db_collection()
    return list(collection.find({}, {"_id": 0}))