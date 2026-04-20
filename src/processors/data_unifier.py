"""
Módulo de Procesamiento y Curación de Datos - HR Pro.
Este es el 'taller mecánico' donde limpiamos, validamos y unimos los fragmentos.
"""

import pandas as pd

def process_chunk_to_df(chunk):
    """
    Toma un lote de mensajes, los limpia y los une por identidad (Pasaporte).
    """
    if not chunk:
        return pd.DataFrame()

    # 1. ENTRADA: Convertimos el saco de mensajes en una tabla
    df = pd.DataFrame(chunk)

    # 2. LIMPIEZA INICIAL: Estándar de texto profesional
    # Eliminamos espacios invisibles y ponemos nombres en formato Título (Juan Pérez)
    text_cols = ['Name', 'Lastname', 'Fullname', 'City', 'Address', 'Job', 'Company']
    for col in text_cols:
        if col in df.columns:
            # astype(str) asegura que no falle si hay un nulo, strip quita espacios
            df[col] = df[col].astype(str).str.strip().str.title()

    # 3. NORMALIZACIÓN FINANCIERA: Asegurar que el sueldo sea un número real
    if 'Salary' in df.columns:
        # 'coerce' convierte errores (como si llega una palabra) en un vacío (NaN)
        df['Salary'] = pd.to_numeric(df['Salary'], errors='coerce')

    # 4. MAPEADO DE IDENTIDAD (El "Traductor")
    # Si tenemos mensajes que tienen Passport y Fullname a la vez, creamos un mapa.
    # Esto nos permite recuperar el Pasaporte en mensajes que solo traen el Nombre.
    if 'Passport' in df.columns and 'Fullname' in df.columns:
        # Creamos un diccionario {Nombre: Pasaporte}
        mapeo_id = df.dropna(subset=['Passport', 'Fullname']).set_index('Fullname')['Passport'].to_dict()
        # Rellenamos los pasaportes vacíos usando el nombre como puente
        df['Passport'] = df['Passport'].fillna(df['Fullname'].map(mapeo_id))

    # 5. UNIFICACIÓN (EL PEGAMENTO): 
    # Agrupamos todo por Pasaporte. 'first()' rescata el primer dato válido de cada fragmento.
    if 'Passport' in df.columns:
        # El reset_index() devuelve la tabla a su formato estándar de filas
        unified_df = df.groupby('Passport').first().reset_index()
        
        # 6. FILTRO DE CALIDAD FINAL:
        # No permitimos registros sin pasaporte en el SQL Warehouse.
        return unified_df.dropna(subset=['Passport'])
    
    return df