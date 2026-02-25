# Arquitetura Atual da API

## Visao de alto nivel

Fluxo atual de inicializacao:

1. `main.py` inicia o `uvicorn` com auto-reload.
2. `uvicorn` carrega `app.run:app`.
3. `app/run.py` garante que os diretorios de foto existem (`ensure_photo_directories`).
4. `app/run.py` cria a app FastAPI.
5. `app/run.py` aplica CORS via `setup_cors`.
6. `app/run.py` registra os routers `health` e `photos`.

## Componentes principais

- `app/run.py`: composicao da aplicacao e registro das rotas.
- `app/core/settings.py`: leitura do `.env` e valores default.
- `app/core/ai_config.py`: normalizacao das configuracoes da IA/OpenAI.
- `app/core/storage.py`: resolucao de paths e bootstrap de diretorios.
- `app/controllers/image_agent.py`: controller fino que delega para service.
- `app/services/image_generation_service.py`: integracao OpenAI + fallback.
- `app/routers/health.py`: endpoints basicos (`/` e `/health`).
- `app/routers/photos.py`: upload, processamento, listagem e download de fotos.
- `app/models/photo_models.py`: schemas de sucesso e erro para Swagger.

## Fluxo de requisicao

```text
Client -> FastAPI (app/run.py) -> Router (app/routers/*) -> Response
```

Fluxo de processamento de IA:

```text
Router (/photos/process) -> Controller (image_agent) -> Service (image_generation_service) -> OpenAI/Fallback
```

## Fluxo de arquivos de imagem

```text
POST /photos/input -> app/data/input/input_photo.<ext> (substitui anterior)
POST /photos/process -> app/data/output/output_photoN.<ext> (salva e retorna arquivo)
GET /photos/output -> lista arquivos em app/data/output
GET /photos/output/{photo_name} -> retorna arquivo por nome base
```

## Regras atuais de armazenamento

- `app/data/input`: sempre 1 foto de entrada (ultima enviada).
- `app/data/output`: multiplas fotos geradas pela IA.
- nomes e paths podem ser configurados via variaveis de ambiente.

## Arquitetura planejada (VCM)

O projeto ja possui os diretorios para VCM:

- `views/`
- `controllers/`
- `models/`

Eles serao preenchidos conforme novos casos de uso forem entrando.
