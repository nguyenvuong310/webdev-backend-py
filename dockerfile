# Stage 1: Build stage
FROM python:3.11 AS builder

WORKDIR /app

COPY requirements.txt .

RUN pip install --user --no-cache-dir -r requirements.txt



FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /root/.local /root/.local

ENV PATH=/root/.local/bin:$PATH

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]