import pandas as pd
import numpy as np # <--- Necesario para detectar los huecos
import re

class DataProcessor:
    def __init__(self):
        self.required_fields = ['passport', 'fullname', 'iban', 'salary', 'city', 'ipv4']

    def _to_snake_case(self, name):
        name = str(name).lower().replace(" ", "_")
        return name

    def clean_batch(self, batch):
        """
        Toma un lote de mensajes crudos, los limpia y los prepara.
        """
        # 1. PARCHE DE SEGURIDAD: 
        # Antes de entrar en Pandas, convertimos cualquier lista en un valor simple.
        # Esto evita el error 'unhashable type: list'.
        for msg in batch:
            for key, value in msg.items():
                if isinstance(value, list):
                    msg[key] = value[0] if len(value) > 0 else None
        df = pd.DataFrame(batch)
        df = df.drop_duplicates()
        df.columns = [self._to_snake_case(col) for col in df.columns]

        # 2. Aseguramos que 'fullname' exista en el DataFrame antes de operar
        if 'fullname' not in df.columns:
            df['fullname'] = np.nan

        # 3. Unificación de nombres
        if 'name' in df.columns and 'last_name' in df.columns:
            mask = df['fullname'].isna() & df['name'].notna() & df['last_name'].notna()
            df.loc[mask, 'fullname'] = df['name'].astype(str) + " " + df['last_name'].astype(str)

        # 4. Limpieza de Salario con conversión a número real
        if 'salary' in df.columns:
            # Quitamos símbolos
            df['salary'] = df['salary'].replace(r'[^\d.]', '', regex=True)
            # Forzamos a que sea un número (si hay basura, pondrá NaN)
            df['salary'] = pd.to_numeric(df['salary'], errors='coerce')

        # 5. Limpieza de strings
        df = df.map(lambda x: x.strip() if isinstance(x, str) else x)

        # --- EL TRUCO SENIOR: Convertir NaNs en None ---
        # Python 'None' es el vacío real que MongoDB y SQL entienden perfectamente.
        # np.nan es un objeto molesto que da falsos positivos.
        df = df.replace({np.nan: None})

        return df.to_dict('records')

    def is_complete(self, person_doc):
        """
        Verifica si el puzzle está completo y NO contiene 'nan' o 'None'
        """
        for field in self.required_fields:
            val = person_doc.get(field)
            # Si el valor es None, o es el string "nan", el puzzle no vale.
            if val is None or str(val).lower() == "nan" or val == "":
                return False
        return True