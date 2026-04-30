FROM python:3.12-slim

# Evita archivos .pyc y buffering de logs
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Instala uv
RUN pip install uv

# Copia solo los ficheros de dependencias primero (mejor cache de capas)
COPY pyproject.toml uv.lock* ./

# Instala dependencias sin las de dev
RUN uv sync --frozen --no-dev

# Copia el resto del código
COPY . .

# Crea la carpeta de logs
RUN mkdir -p logs

CMD ["uv", "run", "python", "-m", "src.main"]