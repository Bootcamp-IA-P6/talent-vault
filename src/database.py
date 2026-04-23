import os
from pymongo import MongoClient
from sqlalchemy import create_engine
from dotenv import load_dotenv

# Cargamos las variables del archivo .env
load_dotenv()

class DatabaseManager:
    def __init__(self):
        # 1. Conexión a MongoDB (Almacén de piezas sueltas)
        # Usamos el URI que definimos en el .env
        self.mongo_client = MongoClient(os.getenv("MONGO_URI"))
        self.mongo_db = self.mongo_client[os.getenv("MONGO_DB", "talent_vault_raw")]
        self.raw_collection = self.mongo_db["raw_messages"]

        # 2. Conexión a SQL (Vitrina de resultados)
        # SQLAlchemy nos permite hablar con SQL de forma elegante
        self.sql_engine = create_engine(os.getenv("DATABASE_URL"))

    def save_to_mongo(self, data):
        """Guarda el mensaje tal cual llega de Kafka"""
        try:
            self.raw_collection.insert_one(data)
        except Exception as e:
            print(f"❌ Error guardando en Mongo: {e}")

    def get_sql_engine(self):
        return self.sql_engine