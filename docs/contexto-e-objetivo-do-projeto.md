# Contexto e Objetivo do Projeto

## Estado atual

Projeto FastAPI estruturado para pipeline de imagens com:

- ponto de entrada em `main.py` (raiz);
- aplicacao HTTP em `app/run.py`;
- configuracao por variaveis de ambiente em `app/core/settings.py`;
- CORS centralizado em `app/core/cors.py`;
- gerenciamento de diretorios de arquivos em `app/core/storage.py`;
- contratos de dados em `app/models/photo_models.py`;
- rotas centralizadas em `app/routers`.

Capacidades ja implementadas:

- upload de uma unica foto de entrada (substitui a anterior);
- processamento da foto de input via agente placeholder;
- listagem das fotos geradas;
- download de foto gerada por nome base (sem extensao);
- criacao automatica dos diretorios de armazenamento ao subir a API.

## Objetivo geral

Construir uma API para processamento e transformacao de imagens com IA, com arquitetura simples de manter e pronta para evolucao.

## Objetivos tecnicos imediatos

- manter estrutura organizada por responsabilidade;
- padronizar configuracao por `.env`;
- permitir evolucao incremental sem refatoracao pesada;
- manter padrao de nomes de pastas e rotas em ingles;
- garantir documentacao de payloads e erros no Swagger/ReDoc.
