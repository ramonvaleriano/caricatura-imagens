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

Resposta de sucesso (200):

```json
{
  "message": "Foto de entrada salva com sucesso.",
  "file_name": "input_photo.jpg",
  "format": "jpg",
  "location": "app/data/input/input_photo.jpg"
}
```

Possiveis erros: `400`, `415`, `422`, `500`.

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

Possiveis erros: `500`.

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

## Swagger

- URL: `http://localhost:8000/docs`
- URL ReDoc: `http://localhost:8000/redoc`
- Tags atuais: `Default`, `Photos`
