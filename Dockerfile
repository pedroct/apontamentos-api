FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

RUN adduser --disabled-password --gecos "" appuser
WORKDIR /app

RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml ./
RUN pip install --no-cache-dir pip==24.2 uv \
 && uv pip install --system "fastapi[all]" "pydantic-settings" "python-jose[cryptography]" \
    "httpx" "psycopg[binary]" "sqlalchemy" "alembic" "loguru"

COPY app ./app
# garanta que os arquivos de migration vão para /app
COPY alembic.ini /app/alembic.ini
COPY alembic /app/alembic
USER appuser
EXPOSE 8000
CMD ["python","-m","uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
