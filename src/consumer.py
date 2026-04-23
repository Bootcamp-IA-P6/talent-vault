import json
from kafka import KafkaConsumer
import os

class TalentVaultConsumer:
    def __init__(self, topic, bootstrap_servers):
        # Configuramos el receptor de la radio (Kafka)
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='earliest', # Empieza desde el principio si es la primera vez
            enable_auto_commit=True       # Marca los mensajes como "leídos" automáticamente
        )

    def consume_batches(self, batch_size=50):
        """
        Lee mensajes de Kafka y los devuelve en grupos (chunks).
        Esto es mucho más eficiente que procesar uno por uno.
        """
        batch = []
        for message in self.consumer:
            batch.append(message.value)
            
            # Cuando el lote está lleno, lo entregamos para procesar
            if len(batch) >= batch_size:
                yield batch
                batch = [] # Vaciamos el lote para el siguiente grupo