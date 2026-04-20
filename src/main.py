"""
Punto de entrada principal del Pipeline de HR Pro.
"""
from src.extractors.kafka_consumer import HRDataConsumer
from src.loaders.mongo_loader import MongoLoader
from src.loaders.sql_loader import SQLLoader
from src.processors.data_unifier import process_chunk_to_df

def main():
    # --- 1. CONFIGURACIÓN ---
    KAFKA_TOPIC = "hr_data_topic"
    BOOTSTRAP_SERVERS = "localhost:9092"
    MONGO_URI = "mongodb://localhost:27017"
    SQL_URI = "postgresql://user:pass@localhost:5432/hr_db"
    
    CHUNK_SIZE = 100  # Procesamos de 100 en 100 para ser eficientes
    buffer = []       # Nuestro saco temporal (Chunk)

    # --- 2. INSTANCIACIÓN DE HERRAMIENTAS ---
    consumer = HRDataConsumer(KAFKA_TOPIC, BOOTSTRAP_SERVERS)
    mongo_db = MongoLoader(MONGO_URI, "hr_pro_db", "raw_messages")
    sql_db = SQLLoader(SQL_URI)

    print("🚀 Pipeline de HR Pro Iniciado. Esperando datos...")

    # --- 3. BUCLE ETL EN TIEMPO REAL ---
    for raw_message in consumer.listen():
        
        # PASO E (Extract) & L1 (Load Raw): 
        # Guardamos en el Data Lake inmediatamente por seguridad
        mongo_db.save_raw(raw_message)
        
        # PASO T (Transform): 
        # Añadimos el mensaje a nuestro saco para el procesamiento por lotes
        buffer.append(raw_message)

        # Si el saco llega al tamaño deseado, procesamos el lote (Chunk)
        if len(buffer) >= CHUNK_SIZE:
            print(f"📦 Procesando lote de {CHUNK_SIZE} mensajes...")
            
            # Unificamos las piezas de los mensajes en una tabla limpia
            unified_df = process_chunk_to_df(buffer)
            
            # PASO L2 (Load Clean):
            # Guardamos la tabla unificada en el archivador SQL
            sql_db.save_unified_data(unified_df, "unified_employees")
            
            # Vaciamos el saco para los siguientes 100 mensajes
            buffer.clear()
            print("✅ Lote procesado y guardado.")

if __name__ == "__main__":
    main()