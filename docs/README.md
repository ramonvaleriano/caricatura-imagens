# Documentacao do Projeto

Esta pasta concentra a documentacao funcional, tecnica e operacional da API.

## Setup rapido (venv, libs e execucao)

Processo recomendado para preparar o ambiente local:

1. Entre na raiz do projeto:

```bash
cd /home/ramonvaleriano/projetos/caricatura-imagens
```

2. Crie um ambiente virtual local (venv):

```bash
python3 -m venv venv
```

3. Ative o ambiente virtual:

Linux/macOS:

```bash
source venv/bin/activate
```

Windows (PowerShell):

```powershell
venv\\Scripts\\Activate.ps1
```

4. Instale as dependencias via `requirements.txt`:

```bash
pip install -r requirements.txt
```

5. Rode a API:

```bash
python3 main.py
```

6. Valide se subiu:

- Swagger: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`
- Health: `http://localhost:8000/health`

Boas praticas:

- use sempre o `venv` deste projeto antes de instalar libs;
- nao instale dependencias globalmente para este projeto;
- adicione/atualize libs apenas via `requirements.txt`.

## Documentos disponiveis

1. `contexto-e-objetivo-do-projeto.md`
2. `arquitetura-atual-da-api.md`
3. `estrutura-de-diretorios.md`
4. `configuracao-de-ambiente.md`
5. `guia-de-execucao-local.md`
6. `endpoints-e-contratos-atuais.md`
7. `diagnostico-e-troubleshooting.md`
8. `plano-de-evolucao-do-projeto.md`

## Ordem recomendada de leitura

1. Contexto e objetivo
2. Arquitetura atual
3. Estrutura de diretorios
4. Configuracao de ambiente
5. Guia de execucao
6. Endpoints e contratos
7. Diagnostico e troubleshooting
8. Plano de evolucao

## Escopo atual documentado

- API FastAPI com inicializacao em `main.py` e app em `app/run.py`.
- rotas padrao (`/` e `/health`) e rotas de fotos (`/photos/*`).
- armazenamento de arquivos em `app/data/input` e `app/data/output`.
- configuracao via `.env` com carga central em `app/core/settings.py`.
- `load_dotenv(..., override=True)` para priorizar valores do `.env`.
- suporte a CORS e upload de arquivo `multipart/form-data`.
- integracao de IA com OpenAI (ativada por `OPENAI_ENABLED`).
- prompts de IA versionados em `app/prompts/*.md` (fora do `.env`).
- separacao de responsabilidade em `controllers` (fino) e `services` (regra de negocio).
- estrutura de logs central com cobertura em startup, rotas, controller e service.
