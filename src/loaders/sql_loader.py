from sqlalchemy import create_engine

class SQLLoader:
    def __init__(self, connection_string):
        # El engine es el "puente" hacia la base de datos (Postgres o MySQL)
        self.engine = create_engine(connection_string)

    def save_unified_data(self, df, table_name):
        """
        Toma un DataFrame de Pandas (el rompecabezas armado)
        y lo guarda de golpe en una tabla SQL.
        """
        try:
            # 'if_exists=append' significa: si la tabla ya existe, añade los datos al final
            df.to_sql(table_name, con=self.engine, if_exists='append', index=False)
            print(f"✅ {len(df)} registros guardados en SQL.")
        except Exception as e:
            print(f"❌ Error al guardar en SQL: {e}")