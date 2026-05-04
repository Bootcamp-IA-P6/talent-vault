FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml uv.lock* ./
RUN pip install uv && uv sync --frozen

COPY datagen/ ./datagen/

CMD ["uv", "run", "python", "datagen/kafka_push.py"]