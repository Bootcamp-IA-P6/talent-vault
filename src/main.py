import os
import time
from database import DatabaseManager
from processor import DataProcessor
from consumer import TalentVaultConsumer
from dotenv import load_dotenv

load_dotenv()

def run_pipeline():
    # Inicialización
    db = DatabaseManager()
    proc = DataProcessor()
    consumer = TalentVaultConsumer(
        topic=os.getenv("KAFKA_TOPIC_NAME"),
        bootstrap_servers=os.getenv("KAFKA_BOOTSTRAP_SERVERS")
    )

    print("🚀 Fábrica 'Talent Vault' en marcha. Armando puzzles...")

    # Flujo continuo
    for batch in consumer.consume_batches(batch_size=50):
        # PASO 1: Limpieza profunda (Tu código con Pandas)
        # --- NUEVO: Integración de tu lógica de limpieza ---
        cleaned_msgs = proc.clean_batch(batch)
        
        # PASO 2: El Pegamento (Transformación e Ingestión Cruda)
        # --- NUEVO: Aquí unimos las piezas en MongoDB ---
        for msg in cleaned_msgs:
            db.update_person(msg)
            
        print(f"📦 Lote de {len(batch)} procesado y unido en MongoDB.")

        # PASO 3: ¿Graduación a SQL? (Fase Final)
        # --- NUEVO: Verificamos si hay alguien listo para la vitrina ---
        completed = db.get_completed_puzzles(proc.required_fields)
        if completed:
            print(f"🎓 ¡Encontrados {len(completed)} puzzles completos! Listos para SQL...")
            # Aquí llamaremos a la función de carga SQL en el siguiente paso.

if __name__ == "__main__":
    run_pipeline()