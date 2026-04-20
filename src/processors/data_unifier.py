import pandas as pd

def process_chunk_to_df(chunk):
    """
    Transforma una lista de mensajes (chunk) en una tabla unificada.
    Usa el Pasaporte como clave de unión.
    """
    if not chunk:
        return pd.DataFrame() # Si el saco está vacío, devolvemos tabla vacía

    # 1. Convertimos la lista de diccionarios en una tabla (DataFrame)
    df = pd.DataFrame(chunk)

    # 2. El Pegamento: Agrupamos por 'Passport'.
    # Como los datos vienen fragmentados, 'first()' toma el primer valor 
    # que encuentre para cada columna (Nombre, Sueldo, etc.) de esa persona.
    if 'Passport' in df.columns:
        unified_df = df.groupby('Passport').first().reset_index()
        # Eliminamos filas que no tengan pasaporte (no son válidas para el warehouse)
        return unified_df.dropna(subset=['Passport'])
    
    return df