import json
from kafka import KafkaConsumer

class HRDataConsumer:
    """Clase para conectarse a Kafka y consumir mensajes en tiempo real."""
    
    def __init__(self, topic, bootstrap_servers):
        # Configuramos la conexión al buzón (Kafka)
        self.consumer = KafkaConsumer(
            topic,
            bootstrap_servers=bootstrap_servers,
            auto_offset_reset='earliest', # Si nos desconectamos, empezamos donde lo dejamos
            # Convertimos los datos de 'bytes' a un diccionario de Python (JSON)
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )

    def listen(self):
        """Generador que entrega mensajes de uno en uno según llegan."""
        print("📡 Conectado a Kafka. Escuchando mensajes...")
        for message in self.consumer:
            # 'yield' es clave: entrega el dato y se queda esperando el siguiente
            # sin consumir toda la memoria RAM.
            yield message.value