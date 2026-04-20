from pymongo import MongoClient

class MongoLoader:
    """Clase para persistir datos crudos (Raw Data) en MongoDB."""

    def __init__(self, uri, db_name, collection_name):
        # Establecemos conexión con el servidor de MongoDB
        self.client = MongoClient(uri)
        # Seleccionamos la base de datos y la colección (la tabla NoSQL)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def save_raw(self, data):
        """Guarda el mensaje tal cual llega, sin procesar."""
        try:
            self.collection.insert_one(data)
        except Exception as e:
            print(f"❌ Error al guardar en Data Lake (Mongo): {e}")