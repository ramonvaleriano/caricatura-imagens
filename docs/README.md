# Documentacao do Projeto

Esta pasta concentra a documentacao funcional, tecnica e operacional da API.

## Documentos disponiveis

1. `contexto-e-objetivo-do-projeto.md`
2. `arquitetura-atual-da-api.md`
3. `estrutura-de-diretorios.md`
4. `configuracao-de-ambiente.md`
5. `guia-de-execucao-local.md`
6. `endpoints-e-contratos-atuais.md`
7. `diagnostico-e-troubleshooting.md`
8. `plano-de-evolucao-do-projeto.md`

## Ordem recomendada de leitura

1. Contexto e objetivo
2. Arquitetura atual
3. Estrutura de diretorios
4. Configuracao de ambiente
5. Guia de execucao
6. Endpoints e contratos
7. Diagnostico e troubleshooting
8. Plano de evolucao

## Escopo atual documentado

- API FastAPI com inicializacao em `main.py` e app em `app/run.py`.
- rotas padrao (`/` e `/health`) e rotas de fotos (`/photos/*`).
- armazenamento de arquivos em `app/data/input` e `app/data/output`.
- configuracao via `.env` com carga central em `app/core/settings.py`.
- `load_dotenv(..., override=True)` para priorizar valores do `.env`.
- suporte a CORS e upload de arquivo `multipart/form-data`.
- integracao de IA com OpenAI (ativada por `OPENAI_ENABLED`).
- prompts de IA versionados em `app/prompts/*.md` (fora do `.env`).
- separacao de responsabilidade em `controllers` (fino) e `services` (regra de negocio).
- estrutura de logs central com cobertura em startup, rotas, controller e service.
