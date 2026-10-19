# 1. - API structure

Contexto: @escopo.md

Objetivo: Me auxilie no desenvolvimento do backend da aplicação, quero que comece estruturando o código em 'api/' com uma api básica com FastApi, leitura de variáveis de ambiente, um endpoint de health check, .gitignore.

Resposta: Código estruturado da api do projeto.

# 2. - API LLM

Contexto: Habilitaremos o agente LLM na api 

Objetivos:

- Instacie e configure o agente LLM e RAG usando langchain e FAISS.

- Configure um fluxo simples para receber mensagem, buscar no RAG e responder a resposta para o usuário.

- Estruturar resposta conforme escopo do projeto

- Mantenha um código simples, refatorações serão feitas em fase futuras

- Atualize requirements e .env.example

- O LLM será rodado local usando o ollama

# 3. Streamlit structure

Contexto: @escopo.md e @schemas.py 

Objetivo: Com base no escopo e nos schemas da api, crie o frontend do chatbot.

Estilo: Crie o projeto frontend usando Streamlit, projeto simples com a tela do projeto e a interação com a api.

Resposta: Projeto estruturado em 'web/'.
