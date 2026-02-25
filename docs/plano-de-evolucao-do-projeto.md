# Plano de Evolucao do Projeto

## Status atual (ja concluido)

1. estrutura base da API com FastAPI.
2. entrypoint com auto-reload (`main.py`).
3. rotas implementadas:
- `GET /`
- `GET /health`
- `POST /photos/input`
- `POST /photos/process`
- `GET /photos/output`
- `GET /photos/output/{photo_name}`
4. configuracao de CORS.
5. configuracao por `.env` em `app/core/settings.py`.
6. diretorios de dados em `app/data/input` e `app/data/output`.
7. integracao OpenAI estruturada com fallback controlado por `OPENAI_ENABLED`.
8. prompts da IA externalizados em `app/prompts/*.md`.
9. logs em startup, rotas, controller e service.
10. contrato de erros padronizado com `APIErrorResponse`.

## Proxima fase (prioridade alta)

1. extrair mais regra de negocio de `app/routers/photos.py` para services dedicados.
2. criar testes automatizados:
- unitarios para `core` e `service`;
- integracao para rotas principais.
3. adicionar validacao de upload mais robusta:
- tamanho maximo do arquivo;
- validacao de mime type real.

## Fase de robustez de IA

1. retries com backoff no provider.
2. timeout configuravel por ambiente.
3. melhor parse de resposta do provider para formatos adicionais.
4. estrategia para multi-provider (OpenAI + fallback local desacoplado).

## Fase de operacao

1. logs estruturados (JSON) opcionais para producao.
2. metricas basicas de processamento por rota.
3. tracing simples do fluxo `upload -> process -> output`.

## Fase de seguranca e producao

1. autenticacao das rotas de escrita/processamento.
2. rate limiting.
3. CORS restritivo por ambiente.
4. politicas de retencao/limpeza de `app/data/output`.
