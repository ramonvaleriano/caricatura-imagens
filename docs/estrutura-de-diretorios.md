# Estrutura de Diretorios do Projeto

```text
caricatura-imagens/
├── .vscode/
│   ├── launch.json          # atalhos de run/debug no VS Code
│   └── settings.json        # interpretador/env padrao
├── app/
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── image_agent.py  # controller fino para fluxo do agente
│   ├── core/
│   │   ├── cors.py         # configuracao de CORS
│   │   ├── settings.py     # variaveis de ambiente
│   │   ├── ai_config.py    # configuracao dedicada da IA/OpenAI
│   │   └── storage.py      # paths e operacoes de diretorios de fotos
│   ├── data/
│   │   ├── input/          # guarda apenas 1 foto de entrada
│   │   │   └── .gitkeep
│   │   └── output/         # guarda N fotos geradas pela IA
│   │       └── .gitkeep
│   ├── models/
│   │   └── photo_models.py # contratos das rotas de fotos
│   ├── services/
│   │   ├── __init__.py
│   │   └── image_generation_service.py # regras da integracao de IA
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py       # rotas basicas da API
│   │   └── photos.py       # upload/listagem/download de fotos
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
- controllers devem ser finos e delegar regra para `services`;
- regras de negocio e integracoes externas entram em `services`;
- modelos de entrada/saida entram em `models`;
- arquivos de entrada e saida de imagem ficam em `app/data`;
- nomes de pastas/rotas de API devem permanecer em ingles.
