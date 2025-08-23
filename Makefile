run:
\tuvicorn app.main:app --reload --host 0.0.0.0 --port 8001
db-up:
\tdocker compose -f docker-compose.dev.yml up -d
db-down:
\tdocker compose -f docker-compose.dev.yml down
fmt:
\truff check --fix .
\tblack .
lint:
\truff check .
\tblack --check .
test:
\tpytest -q
