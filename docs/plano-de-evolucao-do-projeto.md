# Plano de Evolucao do Projeto

## O que iremos fazer

1. Estruturar modulo de processamento de imagem.
2. Criar rotas de upload/transformacao.
3. Implementar camada de servico/controlador.
4. Integrar provider de IA.
5. Persistir metadados das requisicoes.
6. Adicionar autenticacao e controle de acesso.
7. Criar testes automatizados.

## Como iremos fazer

### Fase 1 - Base de dominio

- definir contratos de request/response em `models`;
- criar controllers para regras de negocio;
- adicionar routers especificos por recurso (`images`, `jobs`, etc.).

### Fase 2 - Integracao IA

- encapsular chamadas de IA em modulo dedicado;
- tratar timeout, retries e erros de provider;
- separar processamento sincrono de assincrono.

### Fase 3 - Qualidade e operacao

- incluir testes unitarios e de integracao;
- adicionar logs estruturados;
- preparar configuracoes por ambiente (dev/hml/prod).

### Fase 4 - Producao

- endurecer seguranca (auth, limites, CORS restritivo);
- configurar deploy e observabilidade;
- documentar versao de API e estrategia de evolucao.
