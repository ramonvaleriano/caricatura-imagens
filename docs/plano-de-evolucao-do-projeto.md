# Plano de Evolucao do Projeto

## Status atual

Concluido nesta fase inicial:

1. estrutura base da API com FastAPI;
2. rotas de healthcheck e rota padrao;
3. rotas de fotos (`/photos/input`, `/photos/output`, `/photos/output/{photo_name}`);
4. configuracao de CORS;
5. configuracao de ambiente via `.env`;
6. estrutura de armazenamento em `app/data/input` e `app/data/output`;
7. documentacao OpenAPI com respostas de sucesso e erro.

## Como iremos fazer

### Fase 1 - Base de dominio

- consolidar padrao VCM em casos de uso reais;
- mover regras de negocio de roteador para `controllers`;
- definir nomenclatura final dos recursos (`images`, `jobs`, `providers`).

### Fase 2 - Integracao IA

- encapsular chamadas de IA em modulo dedicado;
- tratar timeout, retries e erros de provider;
- separar processamento sincrono de assincrono.

### Fase 3 - Qualidade e operacao

- incluir testes unitarios e de integracao;
- adicionar logs estruturados;
- adicionar validacoes extras de arquivo (mime type, tamanho maximo);
- preparar configuracoes por ambiente (dev/hml/prod).

### Fase 4 - Producao

- endurecer seguranca (auth, limites, CORS restritivo);
- configurar deploy e observabilidade;
- documentar versao de API e estrategia de evolucao.
