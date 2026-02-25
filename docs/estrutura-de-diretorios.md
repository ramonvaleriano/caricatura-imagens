# Estrutura de Diretorios do Projeto

```text
caricatura-imagens/
├── app/
│   ├── controllers/        # reservado para regras de controle (a preencher)
│   ├── core/
│   │   ├── cors.py         # configuracao de CORS
│   │   └── settings.py     # variaveis de ambiente
│   ├── models/             # reservado para modelos/esquemas (a preencher)
│   ├── routers/
│   │   ├── __init__.py
│   │   └── health.py       # rotas atuais
│   ├── views/              # reservado para camada de view (a preencher)
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
