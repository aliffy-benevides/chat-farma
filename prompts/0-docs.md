# 1. Escopo

## Prompt 1

Contexto: MVP de chatbot (chamado 'Chat Farma') de consulta e confirmação de análises farmacoterapêuticas em que o profissional consiga perguntar, interagir e receber respostas com base exclusivamente em fontes de referência. O MVP terá somente as funcionalidade essenciais, com o chat consultando sites e textos carregados durante o desenvolvimento da plataforma, o carregamento de 'fontes de referência' ficará para versões futuras.

Objetivo: Gere um documento de escopo do MVP com objetivo, requisitos funcionais, não funcionais e o que está fora de escopo.

Estilo: Linguagem técnica, sucinta, em markdown.

Resposta: Documento completo em docs/escopo.md.

## Prompt 2

Remova dos requisitos, pois não serão contemplados agora: 

- a administração interna de fontes,
- registro básico de telemetria,
- RNFs de desempenho, disponibilidade e segurança,
- Mascaramento de dados,
- remova requisitos de histórico,
- remova qualquer questão de observabilidade e logs.

# 2. Backlog

Contexto: @escopo.md, este produto será entregue em 3 releases: core, qualidade (testes) e entrega final.

Objetivo: Criar um backlog simples mínimo com os requisitos técnicos mínimos e critérios de aceite.

Estilo: Checklist Markdown.

Resposta: Documento em docs/backlog.md.

# 3. Desenho de arquitetura

Contexto: Leia a pasta docs para identificar o contexto do projeto. O backed usará FastApi, LangChain e RAG, e o Frontend usará Streamlit.

Objetivo: Gerar um diagrama Mermaid de componentes e fluxo de dados.

Estilo: Simples e legível.

Resposta: Arquivo mermaid com a arquitetura dentro de docs/. 
