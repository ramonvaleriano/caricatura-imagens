# Arquitetura Atual da API

## Visao de alto nivel

Fluxo atual de inicializacao:

1. `main.py` inicia `uvicorn` com `reload=True`.
2. `uvicorn` carrega `app.run:app`.
3. `app/run.py` chama `setup_logging()`.
4. `app/run.py` chama `ensure_photo_directories()`.
5. `app/run.py` cria a app FastAPI.
6. `app/run.py` aplica CORS via `setup_cors(app)`.
7. `app/run.py` registra os routers `health` e `photos`.
8. `app/run.py` registra log de startup com ambiente, modelo e status de OpenAI.

## Componentes principais

- `main.py`: entrypoint de execucao local com auto-reload.
- `app/run.py`: composicao da aplicacao e registro das rotas.
- `app/core/settings.py`: leitura de `.env` via `load_dotenv(..., override=True)` + `os.getenv`.
- `app/core/ai_config.py`: normalizacao de configuracoes da IA/OpenAI.
- `app/core/prompt_loader.py`: leitura e cache dos prompts em `.md`.
- `app/core/logging_config.py`: configuracao central de logging.
- `app/core/cors.py`: configuracao de CORS.
- `app/core/storage.py`: resolucao de paths e bootstrap dos diretorios de dados.
- `app/controllers/image_agent.py`: controller fino que delega para service.
- `app/services/image_generation_service.py`: integracao OpenAI + fallback.
- `app/routers/health.py`: endpoints de status e diagnostico (`GET /` e `GET /health`).
- `app/routers/photos.py`: upload, processamento, listagem e download de fotos.
- `app/models/photo_models.py`: schemas de sucesso/erro para OpenAPI.

## Fluxo de requisicao

```text
Client -> FastAPI (app/run.py) -> Router -> Controller -> Service -> Response
```

Fluxo especifico de processamento com agente:

```text
POST /photos/process
  -> valida arquivo unico em app/data/input
  -> process_image_with_agent(input_photo)
  -> process_image(input_photo)
      -> OPENAI_ENABLED=false: fallback (retorna bytes originais)
      -> OPENAI_ENABLED=true: chama OpenAI Responses API
  -> detecta extensao por magic number (jpg/png/webp)
  -> salva em app/data/output/output_photoN.<ext>
  -> retorna arquivo no response
```

## Contratos entre camadas

- Router: validacao HTTP, mapeamento de status code e serializacao de resposta.
- Controller: orquestracao minima, sem regra de negocio pesada.
- Service: regra de negocio e integracao com provider externo.
- Core: configuracao, infraestrutura de logging/cors/storage/prompt loading.

## Estrutura de logs

Pontos com logs ativos:

- startup da aplicacao;
- chamadas de rota (`/`, `/health`, `/photos/*`);
- entrada no controller do agente;
- decisao de fallback ou chamada OpenAI;
- sucesso/falha na chamada ao provider;
- persistencia da imagem de saida.

Variavel de controle:

- `LOG_LEVEL` (`DEBUG|INFO|WARNING|ERROR`).

## Fluxo de arquivos de imagem

```text
POST /photos/input
  -> app/data/input/input_photo.<ext>
  -> remove arquivo anterior

POST /photos/process
  -> le input unico
  -> processa no agente
  -> salva app/data/output/output_photoN.<ext_detectada>

GET /photos/output
  -> lista arquivos de output

GET /photos/output/{photo_name}
  -> retorna arquivo por nome base
```

## Regras atuais de armazenamento

- `app/data/input`: deve conter apenas 1 imagem ativa.
- `app/data/output`: pode conter varias imagens geradas.
- nomes e paths sao configuraveis via `.env`.
- output e numerado automaticamente (`output_photo1`, `output_photo2`, ...).

## Regras atuais de prompts

- prompts nao ficam em variavel de ambiente;
- prompts vivem em:
  - `app/prompts/image_developer_prompt.md`
  - `app/prompts/image_user_prompt.md`
- leitura centralizada em `app/core/prompt_loader.py`.
