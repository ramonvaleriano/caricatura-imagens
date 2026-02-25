# Configuracao de Ambiente

## Fonte de configuracao

As variaveis sao carregadas de `.env` em `app/core/settings.py`, via `load_dotenv` + `os.getenv`.

## Variaveis atuais

- `APP_NAME`
- `APP_VERSION`
- `ENVIRONMENT`
- `DEBUG`
- `HOST`
- `PORT`
- `CORS_ORIGINS`

## Exemplo de `.env`

```env
APP_NAME="Caricatura Imagens API"
APP_VERSION="0.1.0"
ENVIRONMENT="development"
DEBUG="false"
HOST="0.0.0.0"
PORT="8000"
CORS_ORIGINS="*"
```

## CORS

- `CORS_ORIGINS="*"`: libera todas as origens.
- `CORS_ORIGINS="http://localhost:3000,https://dominio.com"`: restringe por lista.
