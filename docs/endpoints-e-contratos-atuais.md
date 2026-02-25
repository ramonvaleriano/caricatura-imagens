# Endpoints e Contratos Atuais

## Rotas existentes

### `GET /health`

Retorna status basico de saude da API.

Resposta esperada (200):

```json
{
  "status": "ok"
}
```

### `GET /`

Rota padrao inicial.

Resposta esperada (200):

```json
{
  "status": "ok"
}
```

### `POST /photos/input`

Recebe uma foto via `multipart/form-data` no campo `file`.

Regras:

- aceita apenas extensoes de `ALLOWED_INPUT_EXTENSIONS`;
- remove automaticamente a foto anterior no `input`;
- salva com nome `{INPUT_PHOTO_DEFAULT_NAME}.{ext}`.

Request:

- Content-Type: `multipart/form-data`
- Campo obrigatorio: `file`

Resposta de sucesso (200):

```json
{
  "message": "Foto de entrada salva com sucesso.",
  "file_name": "input_photo.jpg",
  "format": "jpg",
  "location": "app/data/input/input_photo.jpg"
}
```

Erros possiveis:

- `400` (`INVALID_FILE_NAME` ou `EMPTY_FILE`)
- `415` (`UNSUPPORTED_FILE_FORMAT`)
- `422` (payload invalido; campo `file` ausente)
- `500` (`FAILED_TO_SAVE_INPUT_PHOTO`)

### `POST /photos/process`

Processa a foto atual no diretorio `input` com o agente e retorna a imagem resultante.

Comportamento por configuracao:

- `OPENAI_ENABLED=false`: fallback (retorna bytes da imagem original).
- `OPENAI_ENABLED=true`: chama OpenAI Responses API para gerar imagem.

Regras:

- nao recebe payload no body;
- exige existir exatamente 1 foto em `app/data/input`;
- detecta automaticamente o formato da imagem retornada (`jpg`, `png`, `webp`);
- salva em `app/data/output` como `output_photoN.<ext_detectada>`;
- retorna o arquivo no response.

Erros possiveis:

- `404` (`INPUT_PHOTO_NOT_FOUND`)
- `409` (`MULTIPLE_INPUT_PHOTOS`)
- `415` (`UNSUPPORTED_INPUT_FILE_FORMAT`)
- `500` (`FAILED_TO_READ_INPUT_DIRECTORY`, `FAILED_TO_PROCESS_IMAGE`, `AGENT_RUNTIME_ERROR`, `EMPTY_AGENT_OUTPUT`, `FAILED_TO_SAVE_OUTPUT_PHOTO`)

Requisitos para IA real:

- `OPENAI_ENABLED=true`
- `OPENAI_API_KEY` configurada
- prompts preenchidos em `app/prompts/image_developer_prompt.md` e `app/prompts/image_user_prompt.md`
- dependencia `openai` instalada

### `GET /photos/output`

Lista todas as fotos geradas no diretorio de saida.

Resposta de sucesso (200):

```json
{
  "total": 2,
  "photos": [
    {
      "file_name": "output_photo1.jpg",
      "format": "jpg"
    },
    {
      "file_name": "output_photo2.png",
      "format": "png"
    }
  ]
}
```

Erros possiveis:

- `500` (`FAILED_TO_LIST_GENERATED_PHOTOS`)

### `GET /photos/output/{photo_name}`

Retorna uma foto gerada pelo nome base, sem exigir extensao.

Exemplo:

- `/photos/output/output_photo1`

Possiveis status:

- `200`: retorna arquivo de imagem
- `400`: `INVALID_PHOTO_NAME`
- `404`: `PHOTO_NOT_FOUND`
- `409`: `AMBIGUOUS_PHOTO_NAME`
- `500`: `FAILED_TO_READ_GENERATED_PHOTO`

## Exemplo de chamadas

Upload:

```bash
curl -X POST "http://localhost:8000/photos/input" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/da/imagem.jpg"
```

Processamento pelo agente:

```bash
curl -X POST "http://localhost:8000/photos/process" --output processed.bin
```

Listagem:

```bash
curl -X GET "http://localhost:8000/photos/output"
```

Download por nome base:

```bash
curl -X GET "http://localhost:8000/photos/output/output_photo1" --output output_photo1.jpg
```

## OpenAPI

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Tags atuais: `Default`, `Photos`
