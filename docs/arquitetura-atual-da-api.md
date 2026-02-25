# Arquitetura Atual da API

## Visao de alto nivel

Fluxo atual de inicializacao:

1. `main.py` inicia o `uvicorn` com auto-reload.
2. `uvicorn` carrega `app.run:app`.
3. `app/run.py` cria a app FastAPI.
4. `app/run.py` aplica CORS via `setup_cors`.
5. `app/run.py` registra os routers.

## Fluxo de requisicao

```text
Client -> FastAPI (app/run.py) -> Router (app/routers/*) -> Response
```

## Arquitetura planejada (VCM)

O projeto ja possui os diretorios para VCM:

- `views/`
- `controllers/`
- `models/`

Eles serao preenchidos conforme novos casos de uso forem entrando.
