# Documentacao do Projeto

Esta pasta concentra toda a documentacao funcional e tecnica da API.

## Documentos disponiveis

1. `contexto-e-objetivo-do-projeto.md`
2. `arquitetura-atual-da-api.md`
3. `estrutura-de-diretorios.md`
4. `configuracao-de-ambiente.md`
5. `guia-de-execucao-local.md`
6. `endpoints-e-contratos-atuais.md`
7. `plano-de-evolucao-do-projeto.md`

## Ordem recomendada de leitura

1. Contexto e objetivo
2. Arquitetura atual
3. Estrutura de diretorios
4. Configuracao de ambiente
5. Guia de execucao
6. Endpoints e contratos
7. Plano de evolucao

## Escopo atual documentado

- API FastAPI com inicializacao em `main.py` e app em `app/run.py`
- rotas padrao (`/` e `/health`) e rotas de fotos (`/photos/*`)
- armazenamento de arquivos em `app/data/input` e `app/data/output`
- configuracao via `.env`
- suporte a CORS e upload de arquivo `multipart/form-data`
