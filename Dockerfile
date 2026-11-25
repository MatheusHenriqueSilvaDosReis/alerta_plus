# syntax=docker/dockerfile:1

# Estágio 1: Build estático do front-end (Expo Web)
FROM node:24-bookworm-slim AS frontend_builder

WORKDIR /app/helsinque

COPY helsinque/package.json helsinque/package-lock.json ./
RUN npm ci

COPY helsinque ./
ENV EXPO_NO_TELEMETRY=1
RUN npx expo export --platform web

# Estágio 2: Runtime único (FastAPI servindo a API + arquivos estáticos do front-end)
FROM python:3.13-slim-bookworm

ENV PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app/viena

COPY viena/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY viena ./
COPY --from=frontend_builder /app/helsinque/dist ./static

EXPOSE 8000

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
