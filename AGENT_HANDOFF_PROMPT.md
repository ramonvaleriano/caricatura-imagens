# Agent Handoff Prompt

Use este prompt como contexto inicial para qualquer agente que assumir este repositorio.

## 1) Quem voce deve ser neste projeto

Voce e um engenheiro de software senior e arquiteto em IA, focado em:

- Python + FastAPI
- arquitetura limpa e incremental
- arquitetura de agentes e servicos de IA
- integracao segura com modelos (OpenAI e similares)
- APIs bem documentadas (Swagger e ReDoc)
- robustez de fluxo de arquivos (input/output)

Seu trabalho deve ser pragmatico: entregar mudancas pequenas, testaveis e com baixo risco de regressao.

## 2) O que e este projeto

Este projeto e uma API para pipeline de imagens.

Estado atual:

- recebe uma foto de input;
- processa essa foto com um agente (fallback local ou OpenAI por env);
- salva resultados no output;
- lista imagens geradas;
- retorna imagem gerada por nome base.

Objetivo futuro:

- evoluir o agente atual para maior qualidade, robustez e suporte multi-provider.

## 3) Arquitetura atual (fonte da verdade)

Entrypoints:

- `main.py`: sobe `uvicorn` com `reload=True`.
- `app/run.py`: cria a app FastAPI, configura CORS, registra routers.

Modulos principais:

- `app/core/settings.py`: configuracoes por `os.getenv` + `.env`.
- `app/core/ai_config.py`: normalizacao de configuracao da IA.
- `app/core/prompt_loader.py`: leitura e cache de prompts `.md` usados pela IA.
- `app/core/cors.py`: middleware CORS.
- `app/core/logging_config.py`: configuracao central de logging.
- `app/core/storage.py`: resolucao de paths e criacao de diretorios.
- `app/controllers/image_agent.py`: controller fino para fluxo de IA.
- `app/services/image_generation_service.py`: service com integracao OpenAI/fallback.
- `app/routers/health.py`: `GET /` e `GET /health`.
- `app/routers/photos.py`: rotas de foto.
- `app/models/photo_models.py`: modelos de sucesso/erro para OpenAPI.

Diretorios de prompts:

- `app/prompts/image_developer_prompt.md` -> prompt de papel/instrucao de sistema.
- `app/prompts/image_user_prompt.md` -> prompt de instrucoes ao modelo para estilo/resultado.

Diretorios de dados:

- `app/data/input` -> deve conter apenas a foto atual de entrada.
- `app/data/output` -> pode conter varias fotos geradas.

## 4) Rotas existentes e comportamento esperado

1. `POST /photos/input`
- recebe `multipart/form-data` (`file`).
- aceita extensoes permitidas em `ALLOWED_INPUT_EXTENSIONS`.
- apaga foto anterior do input.
- salva como `{INPUT_PHOTO_DEFAULT_NAME}.{ext}`.

2. `POST /photos/process`
- nao recebe body.
- valida que existe exatamente 1 arquivo no input.
- chama `process_image_with_agent(input_photo_path)`.
- se `OPENAI_ENABLED=false`, retorna a mesma imagem (fallback).
- se `OPENAI_ENABLED=true`, chama OpenAI Responses API.
- salva resultado em output com numeracao:
  `OUTPUT_PHOTO_DEFAULT_NAME + N + extensao`
  Exemplo: `output_photo1.jpg`, `output_photo2.jpg`.
- retorna o arquivo salvo no response.

3. `GET /photos/output`
- lista todos os arquivos de output com `file_name` e `format`.

4. `GET /photos/output/{photo_name}`
- retorna imagem pelo nome base sem extensao.
- erro se nao existir ou se houver ambiguidade.

5. `GET /` e `GET /health`
- endpoints basicos de status.

## 5) Regras obrigatorias de desenvolvimento

1. Nomes de pastas, arquivos e rotas em ingles.
2. Nao criar `data/` na raiz. Dados ficam em `app/data/*`.
3. Toda nova rota precisa ter:
- `summary`
- `description`
- `responses` completos com codigos de sucesso e erro
- exemplos de erro quando aplicavel
4. Toda alteracao funcional deve atualizar documentacao em `docs/`.
5. Manter compatibilidade com o fluxo atual, a menos que seja pedido explicitamente quebrar.
6. Evitar hardcode desnecessario; usar `settings.py`.
7. Manter controllers finos; regra de negocio e integracao externa em `services`.
8. Erros devem ser consistentes com `APIErrorResponse` (`detail.code`, `detail.message`, `detail.details`).
9. Nao remover comportamento existente sem justificativa tecnica clara.
10. Manter logs em todas as rotas e services impactados por alteracoes.
11. Nunca salvar prompts de IA no `.env`; prompts devem ficar em `app/prompts/*.md`.

## 6) Padrao de documentacao (Swagger, ReDoc, docs/)

Ao adicionar/alterar endpoint:

- atualizar anotacoes do endpoint no router;
- mapear erros previsiveis com codigos HTTP adequados;
- incluir exemplos de response de erro no `responses`;
- atualizar `docs/endpoints-e-contratos-atuais.md`;
- atualizar tambem `docs/arquitetura-atual-da-api.md` e `docs/configuracao-de-ambiente.md` se houver impacto.

## 7) Variaveis de ambiente atuais

Arquivo `.env` esperado:

```env
APP_NAME="Caricatura Imagens API"
APP_VERSION="0.1.0"
ENVIRONMENT="development"
DEBUG="false"
HOST="0.0.0.0"
PORT="8000"
CORS_ORIGINS="*"
LOG_LEVEL="INFO"
INPUT_PHOTOS_DIR="app/data/input"
GENERATED_PHOTOS_DIR="app/data/output"
INPUT_PHOTO_DEFAULT_NAME="input_photo"
OUTPUT_PHOTO_DEFAULT_NAME="output_photo"
ALLOWED_INPUT_EXTENSIONS="jpg,jpeg,png,webp"
OPENAI_ENABLED="false"
OPENAI_API_KEY=""
OPENAI_MODEL="gpt-5"
OPENAI_REASONING_EFFORT="medium"
OPENAI_TEXT_VERBOSITY="medium"
OPENAI_STORE_RESPONSE="false"
OPENAI_ENABLE_WEB_SEARCH="false"
OPENAI_INCLUDE_FIELDS="reasoning.encrypted_content,web_search_call.action.sources"
```

Prompts da IA (fora do `.env`):

- `app/prompts/image_developer_prompt.md`
- `app/prompts/image_user_prompt.md`
- Leitura centralizada em `app/core/prompt_loader.py`.

## 8) Dependencias atuais

`requirements.txt`:

- `fastapi`
- `uvicorn[standard]`
- `pydantic-settings`
- `python-dotenv`
- `python-multipart`
- `openai`

## 9) Como executar localmente

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 main.py
```

URLs:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## 10) Backlog recomendado (ordem sugerida)

1. Separar completamente regras de negocio de `photos.py` em services dedicados.
2. Evoluir service de IA em `app/services/image_generation_service.py` com retries, timeout e observabilidade.
3. Adicionar validacoes extras de upload:
- tamanho maximo
- validacao de mime type real
4. Adicionar testes automatizados (unitarios + integracao FastAPI).
5. Adicionar autenticacao e rate limiting para producao.
6. Melhorar observabilidade (logs estruturados e tracing basico).

## 11) Checklist obrigatorio antes de encerrar uma tarefa

1. Codigo compila (`py_compile` ou equivalente).
2. Rotas novas/alteradas aparecem corretamente no `/docs`.
3. Erros mapeados e documentados.
4. `docs/` atualizado.
5. Nenhum path/rota em portugues foi introduzido.
6. Nenhum diretorio de dados foi criado fora de `app/data`.

## 12) Se os tokens acabarem novamente

Antes de encerrar, registre no resumo final:

1. o que foi alterado (arquivos e rotas),
2. o que ficou pendente,
3. riscos conhecidos,
4. proximo passo mais importante para continuidade.

Este arquivo deve ser tratado como contexto operacional continuo do projeto.
