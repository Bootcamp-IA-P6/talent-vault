from database import DatabaseManager
from consumer import TalentVaultConsumer
import os
from dotenv import load_dotenv

load_dotenv()

def run_pipeline():
    # 1. Inicializamos nuestras herramientas
    db = DatabaseManager()
    
    # Configuramos el consumidor (leyendo del .env)
    consumer = TalentVaultConsumer(
        topic=os.getenv("KAFKA_TOPIC_NAME"),
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    )

    print("🚀 Fábrica 'Talent Vault' en marcha. Esperando manzanas...")

    # 2. Empezamos a recibir lotes de mensajes
    for batch in consumer.consume_batches(batch_size=100):
        print(f"📦 Recibido lote de {len(batch)} mensajes.")
        
        for msg in batch:
            # Paso A: Guardar en crudo en MongoDB (Persistencia inmediata)
            db.save_to_mongo(msg)
            
        print("✅ Lote guardado en MongoDB crudo. Siguiente paso: Transformación...")
        # Aquí es donde llamaremos al procesador más adelante...

if __name__ == "__main__":
    run_pipeline()