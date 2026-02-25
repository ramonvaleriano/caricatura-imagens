# Endpoints e Contratos Atuais

## Rotas existentes

### `GET /health`

Retorna status basico de saude da API.

Resposta esperada:

```json
{
  "status": "ok"
}
```

### `GET /`

Rota padrao inicial.

Resposta esperada:

```json
{
  "status": "ok"
}
```

### `POST /photos/input`

Recebe uma foto via `multipart/form-data` no campo `file`.

Regras:

- aceita apenas extensoes permitidas;
- remove automaticamente a foto anterior de entrada;
- salva a nova foto com nome padrao + extensao original.

Request:

- Content-Type: `multipart/form-data`
- Campo obrigatorio: `file` (arquivo)

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

- `400`: nome de arquivo invalido ou arquivo vazio.
- `415`: formato nao suportado.
- `422`: payload invalido (ex: campo `file` ausente).
- `500`: falha interna ao salvar arquivo.

### `GET /photos/output`

Lista todas as fotos geradas pela IA no diretorio de saida.

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

- `500`: falha interna ao listar arquivos.

### `GET /photos/output/{photo_name}`

Retorna uma foto gerada sem precisar informar extensao.

Exemplo:

- `/photos/output/output_photo1`

Possiveis status:

- `200`: retorna o arquivo de imagem;
- `400`: nome invalido;
- `404`: foto nao encontrada;
- `409`: mais de uma foto com mesmo nome base;
- `500`: falha interna.

## Exemplo de chamadas

Upload:

```bash
curl -X POST "http://localhost:8000/photos/input" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@/caminho/da/imagem.jpg"
```

Listagem:

```bash
curl -X GET "http://localhost:8000/photos/output"
```

Download por nome base:

```bash
curl -X GET "http://localhost:8000/photos/output/output_photo1" --output output_photo1.jpg
```

## Swagger

- URL: `http://localhost:8000/docs`
- URL ReDoc: `http://localhost:8000/redoc`
- Tags atuais: `Default`, `Photos`
