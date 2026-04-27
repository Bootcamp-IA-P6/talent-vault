import os
from pymongo import MongoClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()

class DatabaseManager:
    def __init__(self):
        # Conexión a MongoDB
        self.mongo_client = MongoClient(os.getenv("MONGO_URI"))
        self.mongo_db = self.mongo_client[os.getenv("MONGO_DB", "talent_vault_raw")]
        self.raw_collection = self.mongo_db["raw_messages"]

        # Conexión a SQL (PostgreSQL)
        self.sql_engine = create_engine(os.getenv("DATABASE_URL"))
        self.Session = sessionmaker(bind=self.sql_engine)

    # --- NUEVO: La Lógica del Pegamento (Upsert) ---
    def update_person(self, clean_data):
        """
        Busca a una persona por sus 3 hilos posibles y une la nueva información.
        """
        # 1. Definimos los hilos de identidad
        passport = clean_data.get("passport")
        fullname = clean_data.get("fullname")
        address = clean_data.get("address")

        # 2. Creamos una lista de condiciones de búsqueda (solo con lo que no sea None)
        filters = []
        if passport: filters.append({"passport": passport})
        if fullname: filters.append({"fullname": fullname})
        if address: filters.append({"address": address})

        if not filters:
            # Si el mensaje no tiene ningún identificador (raro), lo guardamos suelto
            self.raw_collection.insert_one(clean_data)
            return

        # 3. EJECUTAMOS EL UPSERT: 
        # Si encuentra a alguien con ese pasaporte O nombre O dirección, le añade 
        # los campos nuevos que traiga 'clean_data'. Si no existe, lo crea.
        result = self.raw_collection.update_one(
            {"$or": filters},
            {"$set": clean_data},
            upsert=True
        )

    # --- NUEVO: Buscador de Puzzles Completos ---
    def get_completed_puzzles(self, required_fields):
        """Busca en Mongo documentos que tengan todos los campos necesarios"""
        query = {field: {"$ne": None} for field in required_fields}
        # Solo traemos los que NO han sido enviados a SQL todavía
        query["processed_sql"] = {"$ne": True}
        return list(self.raw_collection.find(query))

    def mark_as_processed(self, person_id):
        """Marca el puzzle como completado para no duplicar en SQL"""
        self.raw_collection.update_one(
            {"_id": person_id},
            {"$set": {"processed_sql": True}}
        )