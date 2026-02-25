# Estrutura de Diretorios do Projeto

```text
caricatura-imagens/
├── .vscode/
│   ├── launch.json                 # atalhos de run/debug no VS Code
│   └── settings.json               # env e interpretador Python
├── app/
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── image_agent.py          # controller fino do agente
│   ├── core/
│   │   ├── ai_config.py            # normalizacao da configuracao OpenAI
│   │   ├── cors.py                 # configuracao de CORS
│   │   ├── logging_config.py       # configuracao central de logs
│   │   ├── prompt_loader.py        # leitura de prompts em .md
│   │   ├── settings.py             # configuracoes por os.getenv + .env
│   │   └── storage.py              # paths e bootstrap dos diretorios de fotos
│   ├── data/
│   │   ├── input/
│   │   │   └── .gitkeep
│   │   └── output/
│   │       └── .gitkeep
│   ├── models/
│   │   └── photo_models.py         # schemas de resposta e erro
│   ├── prompts/
│   │   ├── image_developer_prompt.md
│   │   └── image_user_prompt.md
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── health.py
│   │   └── photos.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── image_generation_service.py
│   ├── __init__.py
│   └── run.py                      # criacao da app FastAPI
├── docs/
│   ├── README.md
│   ├── arquitetura-atual-da-api.md
│   ├── configuracao-de-ambiente.md
│   ├── contexto-e-objetivo-do-projeto.md
│   ├── diagnostico-e-troubleshooting.md
│   ├── endpoints-e-contratos-atuais.md
│   ├── estrutura-de-diretorios.md
│   ├── guia-de-execucao-local.md
│   └── plano-de-evolucao-do-projeto.md
├── AGENT_HANDOFF_PROMPT.md
├── main.py                         # entrypoint para rodar servidor local
├── requirements.txt
└── .env
```

## Regras de organizacao

- novas rotas entram em `app/routers`.
- configuracoes globais entram em `app/core`.
- controller deve ser fino e delegar para `service`.
- regra de negocio e integracao externa ficam em `app/services`.
- prompts de IA ficam em `app/prompts/*.md`.
- dados de imagem ficam em `app/data/input` e `app/data/output`.
- nomes de diretorios, arquivos e rotas devem permanecer em ingles.

## Regra de dados

- `app/data/input`: manter apenas 1 imagem ativa (ultima enviada).
- `app/data/output`: manter historico de multiplas imagens geradas.
