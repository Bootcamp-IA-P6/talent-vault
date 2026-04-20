🚀 HR Pro: Pipeline de Ingeniería de Datos (Nivel Esencial)
Talent-Vault - Proyecto Educativo AI School

Este repositorio contiene la primera fase del sistema de procesamiento de datos en tiempo real para HR Pro. Hemos transformado el flujo caótico de mensajes fragmentados de Recursos Humanos en una infraestructura de datos sólida y escalable.

🎯 Objetivo de esta fase

Implementar un flujo ETL (Extract, Transform, Load) de "grado industrial" que capture mensajes de Apache Kafka y los persista en una estrategia dual:

Data Lake (MongoDB): Almacenamiento rápido de datos crudos (Raw) para asegurar que no se pierda ninguna información.

Data Warehouse (SQL): Almacenamiento curado y unificado, donde los datos fragmentados se consolidan en un único registro por empleado.

🏗️ Arquitectura del Sistema

Hemos seguido el principio de Responsabilidad Única, dividiendo el sistema en módulos independientes:

Extractor (Capa E): Un consumidor de Kafka que escucha eventos en streaming.

Processor (Capa T): El motor de lógica que utiliza Pandas para limpiar el texto y unir las piezas del rompecabezas (identidad) usando el Pasaporte como clave.

Loaders (Capa L):

MongoLoader: Persistencia inmediata en base de datos NoSQL.

SQLLoader: Carga por lotes (Chunks) en base de datos relacional.

📂 Estructura del Proyecto

hr-pro-pipeline/
├── src/
│   ├── main.py              # Orquestador principal del flujo.
│   ├── extractors/          # Lógica de conexión a fuentes (Kafka).
│   ├── processors/          # Limpieza, unificación y lógica de Chunks.
│   └── loaders/             # Conectores a bases de datos (Mongo/SQL).
├── pyproject.toml           # Gestión de dependencias con 'uv'.
└── README.md
🛠️ Decisiones de Ingeniería (El "Por qué")
1. Estrategia de Chunks (Lotes)

Para evitar saturar la base de datos SQL con miles de pequeñas inserciones, implementamos un Buffer de 100 mensajes. Esto optimiza el rendimiento y reduce la latencia del sistema.

2. Mapeado de Identidad

Debido a la fragmentación del origen (5 esquemas distintos), nuestro procesador realiza un trabajo de "detective de datos":

Utiliza el Passport como llave maestra.

Si un mensaje solo trae el nombre, el sistema busca en el lote actual si existe una relación previa nombre-pasaporte para "curar" el dato antes de guardarlo.

3. Idempotencia y Calidad

El sistema realiza una limpieza de strings (stripping y title case) y validación numérica de sueldos en cada lote, garantizando que el Data Warehouse contenga información lista para el análisis de negocio sin necesidad de limpieza posterior.

🚀 Cómo ejecutarlo

Instalar dependencias:
Asegúrate de tener uv instalado y ejecuta:

uv sync

Configuración:
Asegúrate de tener levantados los servidores de Kafka, MongoDB y PostgreSQL (esto se automatizará en el Nivel Medio con Docker).

Lanzar el Pipeline:

uv run python -m src.main
📈 Próximos Pasos

Nivel Medio: Dockerización total del entorno y sistema de Logs profesionales.

Nivel Avanzado: Implementación de Redis como caché y monitorización con Prometheus.

Desarrollado con ❤️ por el equipo de Talent-Vault.

