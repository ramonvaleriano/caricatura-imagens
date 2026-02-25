# Guia de Execucao Local

## Pre-requisitos

- Python 3.10+
- dependencias instaladas em `requirements.txt`

## Instalar dependencias

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Subir servidor pelo terminal

```bash
python3 main.py
```

## Subir servidor pelo VS Code

Configuracoes ja disponiveis em `.vscode/launch.json`:

- `API: Run (Auto Reload)`
- `API: Debug`

## Validar se subiu corretamente

1. Abrir `http://localhost:8000/docs`
2. Abrir `http://localhost:8000/redoc`
3. Testar `GET /health`

## Modo de desenvolvimento

O `main.py` sobe o `uvicorn` com `reload=True`, entao toda alteracao de codigo reinicia o servidor automaticamente.

## Exemplo rapido de teste via curl

```bash
curl -X GET http://localhost:8000/health
```

```bash
curl -X POST "http://localhost:8000/photos/process" --output processed.jpg
```

## Teste de IA real (OpenAI)

1. Definir no `.env`:
- `OPENAI_ENABLED="true"`
- `OPENAI_API_KEY="<SUA_CHAVE>"`
2. Reiniciar a API
3. Executar `POST /photos/process` novamente
