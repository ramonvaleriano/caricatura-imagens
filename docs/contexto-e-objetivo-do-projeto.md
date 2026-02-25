# Contexto e Objetivo do Projeto

## Estado atual

Projeto FastAPI estruturado para pipeline de imagens com:

- ponto de entrada em `main.py` (raiz);
- aplicacao HTTP em `app/run.py`;
- configuracao por variaveis de ambiente em `app/core/settings.py`;
- carga de `.env` com `override=True` para reduzir conflitos de ambiente local;
- configuracao dedicada da IA em `app/core/ai_config.py`;
- prompts de IA carregados de arquivos `.md` em `app/prompts`;
- CORS centralizado em `app/core/cors.py`;
- logging centralizado em `app/core/logging_config.py`;
- gerenciamento de diretorios de arquivos em `app/core/storage.py`;
- contratos de dados em `app/models/photo_models.py`;
- camada de service para integracao de IA em `app/services/image_generation_service.py`;
- rotas centralizadas em `app/routers`.

Capacidades ja implementadas:

- upload de uma unica foto de entrada (substitui a anterior);
- processamento da foto de input via agente com fallback/local ou OpenAI (por env);
- deteccao automatica da extensao da imagem retornada pelo agente (`jpg`, `png`, `webp`);
- listagem das fotos geradas;
- download de foto gerada por nome base (sem extensao);
- criacao automatica dos diretorios de armazenamento ao subir a API;
- logs em todas as rotas, controller e service para diagnostico rapido.

## Objetivo geral

Construir uma API para processamento e transformacao de imagens com IA, com arquitetura simples de manter e pronta para evolucao.

## Objetivos tecnicos imediatos

- manter estrutura organizada por responsabilidade;
- padronizar configuracao por `.env`;
- permitir evolucao incremental sem refatoracao pesada;
- manter padrao de nomes de pastas e rotas em ingles;
- garantir documentacao de payloads e erros no Swagger/ReDoc;
- manter rastreabilidade de execucao do agente por logs.
