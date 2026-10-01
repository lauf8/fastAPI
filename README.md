# FastAPI + PostgreSQL

Ambiente de desenvolvimento com Python 3.13, PostgreSQL 17 e reload automático.

```bash
cp .env.example .env
docker compose -f dockercompose.yaml up --build -d
```

- API: http://localhost:8000
- Swagger: http://localhost:8000/docs
- Conexão com o banco: http://localhost:8000/health/db

Dentro do Docker, o host do banco é `db`. Na máquina local, use `localhost:5432`.
As credenciais de exemplo são destinadas a desenvolvimento local.

```bash
docker compose -f dockercompose.yaml logs -f api
docker compose -f dockercompose.yaml down
```

O volume preserva os dados ao executar `down`. `down -v` apaga o volume e os dados.
As variáveis POSTGRES inicializam somente um volume vazio. Alterar o arquivo .env não modifica usuários ou senhas de um banco já inicializado.

Se a porta 5432 estiver ocupada, use `127.0.0.1:5433:5432` no serviço db. A API continua usando db:5432.

Docker não estava disponível no ambiente de geração; o projeto não foi executado em contêineres.
