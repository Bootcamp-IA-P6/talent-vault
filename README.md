---

# 🚀 Talent Vault - Sistema ETL de RRHH en Tiempo Real

¡Bienvenidos al proyecto **Talent Vault**! Este sistema está diseñado para capturar, procesar y unificar datos dispersos de recursos humanos provenientes de un flujo continuo de **Apache Kafka**.


1. **Kafka** es el camión que descarga piezas sueltas de forma aleatoria y masiva.
2. **MongoDB** es nuestro almacén de materia prima (Data Lake) donde guardamos todo rápido para que no se pierda.
3. **Python + Pandas** es nuestra mesa de montaje donde unimos las piezas de cada persona.
4. **PostgreSQL** es nuestra vitrina final (Data Warehouse) donde solo hay pasteles terminados y perfectos.

## 🛠️ Stack Tecnológico
Para este proyecto usamos herramientas modernas de ingeniería de datos:
*   **Gestor de Paquetes:** [uv](https://github.com/astral-sh/uv) (Extremadamente rápido, reemplaza a pip).
*   **Contenedores:** Docker & Docker Compose (Imágenes `-slim` para mayor eficiencia).
*   **Cola de Mensajes:** Apache Kafka.
*   **Bases de Datos:** 
    *   MongoDB (Almacenamiento de datos crudos/NoSQL).
    *   PostgreSQL (Almacenamiento de datos estructurados/SQL).
*   **Procesamiento:** Python 3.12 + Pandas (Procesamiento por chunks/lotes).

---

## 📂 Estructura del Proyecto
```text
talent_vault/
├── datagen/          # Generador de datos (Caja negra del cliente)
├── src/
│   ├── main.py       # Orquestador del pipeline
│   ├── consumer.py   # Lógica de consumo de Kafka por lotes
│   ├── database.py   # Gestión de conexiones a Mongo y Postgres
│   └── processor.py  # Cerebro de transformación y limpieza
├── .env              # Variables de entorno (No se sube a Git)
├── docker-compose.yml # Orquestación de infraestructura
└── pyproject.toml    # Dependencias gestionadas por uv
```

---

## 🚀 Guía de Inicio Rápido

### 1. Requisitos Previos
*   Tener instalado **Docker** y **Docker Compose**.
*   Tener instalado **uv**: 
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```

### 2. Configuración del Entorno
Clona el repositorio y prepara el entorno virtual:
```bash
# Sincronizar dependencias
uv sync
```

Crea un archivo `.env` en la raíz con la siguiente configuración:
```env
KAFKA_BOOTSTRAP_SERVERS=localhost:29092
KAFKA_TOPIC_NAME=probando
MONGO_URI=mongodb://admin:password@localhost:27017
MONGO_DB=talent_vault_raw
DATABASE_URL=postgresql://user:password@localhost:5432/talent_vault_clean
```

### 3. Encender la Maquinaria
Levanta la infraestructura (Kafka, Mongo, Postgres y el Generador):
```bash
docker compose up -d
```

### 4. Ejecutar el Pipeline ETL
Una vez que los contenedores estén corriendo, lanza el proceso de ingesta:
```bash
uv run src/main.py
```

---

## 📈 Estados del Proyecto
*   ✅ **Fase 1 (Ingestión):** Conexión a Kafka y persistencia de datos crudos en MongoDB funcionando.
*   ⏳ **Fase 2 (Transformación):** Lógica de unión de mensajes por Pasaporte/Dirección (En desarrollo).
*   ⏳ **Fase 3 (Carga):** Inserción final en PostgreSQL (Pendiente).

---
**Nota de Ingeniería:** Este proyecto prioriza la **eficiencia de memoria**. No cargamos todos los mensajes a la vez; los procesamos en "chunks" (lotes) de 100 mensajes para asegurar que el sistema sea estable incluso con millones de registros.

---

