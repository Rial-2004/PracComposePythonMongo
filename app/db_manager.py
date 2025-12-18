from pymongo import MongoClient
from bson.objectid import ObjectId

def get_db_collection():
    """Establece la conexión con la base de datos MongoDB."""
    client = MongoClient('mongo', 27017, username='user', password='password')
    db = client.school_db
    return db.students

def init_db():
    """Inicializa la base de datos con datos de prueba si está vacía."""
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
    """Inserta un nuevo estudiante en la colección."""
    collection = get_db_collection()
    collection.insert_one({"nombre": nombre, "localidad": localidad, "nota": int(nota)})

def get_all_students():
    """Recupera todos los estudiantes sin el ID interno de Mongo."""
    collection = get_db_collection()
    return list(collection.find({}, {"_id": 0}))

def get_student_by_name(nombre):
    """Busca un estudiante específico por su nombre."""
    collection = get_db_collection()
    return collection.find_one({"nombre": nombre}, {"_id": 0})

def update_student(nombre_original, nuevo_nombre, nueva_localidad, nueva_nota):
    """Actualiza los datos de un estudiante existente."""
    collection = get_db_collection()
    collection.update_one(
        {"nombre": nombre_original},
        {"$set": {
            "nombre": nuevo_nombre,
            "localidad": nueva_localidad,
            "nota": int(nueva_nota)
        }}
    )

def delete_student(nombre):
    """Elimina un estudiante de la base de datos."""
    collection = get_db_collection()
    collection.delete_one({"nombre": nombre})