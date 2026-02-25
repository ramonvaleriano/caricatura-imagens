# Estrutura de Diretorios do Projeto

```text
caricatura-imagens/
├── app/
│   ├── controllers/        # reservado para regras de controle (a preencher)
│   ├── core/
│   │   ├── cors.py         # configuracao de CORS
│   │   ├── settings.py     # variaveis de ambiente
│   │   └── storage.py      # paths e operacoes de diretorios de fotos
│   ├── models/
│   │   └── photo_models.py # contratos das rotas de fotos
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py       # rotas basicas da API
│   │   └── photos.py       # upload/listagem/download de fotos
│   ├── views/              # reservado para camada de view (a preencher)
│   ├── data/
│   │   ├── input/          # guarda apenas 1 foto de entrada
│   │   └── output/         # guarda N fotos geradas pela IA
│   └── run.py              # criacao da app FastAPI
├── docs/                   # documentacao do projeto
├── main.py                 # entrypoint para subir servidor
├── requirements.txt
└── .env
```

## Regra de organizacao

- novas rotas entram em `app/routers`;
- configuracoes globais entram em `app/core`;
- regras de negocio entram em `controllers` quando surgirem;
- modelos de entrada/saida entram em `models`.
