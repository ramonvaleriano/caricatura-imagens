# Contexto e Objetivo do Projeto

## Estado atual

Projeto base em FastAPI com:

- ponto de entrada em `main.py` (raiz);
- aplicacao HTTP em `app/run.py`;
- configuracao por variaveis de ambiente em `app/core/settings.py`;
- CORS centralizado em `app/core/cors.py`;
- rotas centralizadas em `app/routers`.

## Objetivo geral

Construir uma API para processamento e transformacao de imagens com IA, com arquitetura simples de manter e pronta para evolucao.

## Objetivos tecnicos imediatos

- manter estrutura organizada por responsabilidade;
- padronizar configuracao por `.env`;
- permitir evolucao incremental sem refatoracao pesada.
