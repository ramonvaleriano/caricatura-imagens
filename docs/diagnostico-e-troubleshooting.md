# Diagnostico e Troubleshooting

## Objetivo

Este guia acelera diagnostico quando o processamento da imagem nao passa pelo agente ou nao gera output esperado.

## Verificacoes rapidas

1. API subiu sem erro?
- acesse `GET /health`

2. Existe imagem no input?
- `POST /photos/process` exige exatamente 1 arquivo em `app/data/input`

3. IA real esta ativa?
- no `.env`: `OPENAI_ENABLED="true"`
- no startup log: `openai_enabled=true`

4. Chave existe?
- no `.env`: `OPENAI_API_KEY` preenchida

5. Prompts existem e nao estao vazios?
- `app/prompts/image_developer_prompt.md`
- `app/prompts/image_user_prompt.md`

## Como diferenciar fallback vs OpenAI

### Quando cai em fallback

No log do service:

- `Image processed with fallback | reason=OPENAI_DISABLED ...`

### Quando chama OpenAI

No log do service:

- `Calling OpenAI | model=...`
- depois `Image processed with OpenAI | output_size_bytes=...`

## Sequencia de logs esperada para `/photos/process`

1. `Route called | method=POST path=/photos/process`
2. `Processing input photo with agent | ...`
3. `Controller called | controller=image_agent ...`
4. `Service called | service=image_generation_service ...`
5. `Calling OpenAI ...` (se habilitado)
6. `Photo processed | input_file=... output_file=...`

## Erros comuns e acao recomendada

### `INPUT_PHOTO_NOT_FOUND` (404)

Causa:

- nao existe arquivo em `app/data/input`.

Acao:

- enviar uma foto em `POST /photos/input` e repetir `POST /photos/process`.

### `MULTIPLE_INPUT_PHOTOS` (409)

Causa:

- mais de um arquivo em `app/data/input`.

Acao:

- limpar o diretorio e manter apenas um arquivo de entrada.

### `UNSUPPORTED_INPUT_FILE_FORMAT` (415)

Causa:

- extensao fora de `ALLOWED_INPUT_EXTENSIONS`.

Acao:

- usar uma extensao permitida (`jpg`, `jpeg`, `png`, `webp`) ou ajustar `.env`.

### `AGENT_RUNTIME_ERROR` (500)

Causa comum:

- erro retornado pelo provider (chave invalida, permissao, quota, etc).

Acao:

- ler `detail.details.error` da resposta;
- corrigir credencial/configuracao;
- repetir o teste.

### `EMPTY_AGENT_OUTPUT` (500)

Causa:

- provider respondeu sem imagem util.

Acao:

- revisar prompts e logs do service;
- validar se o modelo/config de tools retornam imagem.

### `FAILED_TO_SAVE_OUTPUT_PHOTO` (500)

Causa:

- falha de escrita em disco/permissao.

Acao:

- verificar permissao de escrita em `app/data/output`.

## Checklist de confirmacao final

1. upload retornou 200 em `/photos/input`.
2. process retornou 200 em `/photos/process`.
3. lista retornou arquivo novo em `/photos/output`.
4. download por nome base retornou 200 em `/photos/output/{photo_name}`.
