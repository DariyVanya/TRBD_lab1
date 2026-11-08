FROM python:3.12-slim

WORKDIR /app

RUN pip install --no-cache-dir uv
RUN uv pip install --system --no-cache "kafka-python>=2.0.2,<3"

COPY producer ./producer
COPY consumer ./consumer
COPY scripts ./scripts

CMD ["python", "producer/main.py", "--help"]
