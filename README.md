# <repo>

FastAPI + PostgreSQL (DEV via docker-compose). JWT (OIDC) para SPA e HMAC para webhooks.

## Dev
```bash
cp .env.example .env
# Preencha POSTGRES_PASSWORD no .env do compose dev
docker compose -f docker-compose.dev.yml up -d
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
make run

## Valores específicos por app

- **apontamentos-api**
  - Porta dev API: **8001**
  - Postgres dev: `localhost:5433`, DB `apontamentos_db`
  - `AUTH_AUDIENCE=api://apontamentos`

- **sgs-api**
  - Porta dev API: **8002**
  - Postgres dev: `localhost:5434`, DB `sgs_db`
  - `AUTH_AUDIENCE=api://sgs`

Se quiser, eu já te devolvo tudo zipado com os nomes trocados certinho para **apontamentos-api** e **sgs-api**.
