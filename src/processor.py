import pandas as pd

class DataProcessor:
    def __init__(self):
        # Aquí podríamos definir qué campos son obligatorios
        self.required_keys = ['passport', 'fullname', 'iban', 'salary', 'ipv4']

    def clean_batch(self, batch):
        """
        Toma un lote de mensajes y los convierte en un DataFrame de Pandas
        para poder limpiarlos y agruparlos fácilmente.
        """
        df = pd.DataFrame(batch)
        
        # Ejemplo de limpieza simple: quitar espacios en blanco de los nombres
        if 'fullname' in df.columns:
            df['fullname'] = df['fullname'].str.strip()
            
        return df

    def merge_person_data(self, existing_data, new_piece):
        """
        Lógica para unir las piezas de la manzana.
        Si ya tenemos algo de la persona, le sumamos la nueva pieza.
        """
        # Esta lógica la perfeccionaremos en el siguiente paso
        # Por ahora, solo piensa que 'existing_data' es lo que hay en Mongo
        # y 'new_piece' es lo que acaba de llegar de Kafka.
        combined = {**existing_data, **new_piece}
        return combined