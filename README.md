# Chat Farma (MVP)

O **Chat Farma** é um MVP de chatbot para **consulta e confirmação de análises farmacoterapêuticas**, permitindo que profissionais de saúde (ex.: farmacêuticos clínicos) façam perguntas e recebam respostas **baseadas exclusivamente em fontes de referência curadas** e controladas pela equipe.

Este projeto implementa um fluxo **RAG (Retrieval-Augmented Generation)** com **citações e trechos (snippets)** para rastreabilidade. Caso não exista evidência suficiente no acervo do MVP, o sistema deve **recusar** e orientar a reformulação da pergunta.

## Tecnologias utilizadas

- **Frontend**: Streamlit (UI de chat)
- **Backend**: FastAPI (API HTTP)
- **RAG / Orquestração**: LangChain (camada de retrieval + montagem de prompt)
- **LLM local**: Ollama
- **Containerização**: Docker + Docker Compose

## Pré-requisitos

- **Docker** (Docker Engine)
- **Docker Compose** (plugin `docker compose`)
- (Opcional, para desenvolvimento sem Docker) Python 3.x

## Instalação e execução (Docker)

1. **Clone o repositório**
   ```sh
   git clone https://github.com/aliffy-benevides/chat-farma.git
   cd chat-farma
   ```

2. **Crie os arquivos `.env` a partir dos exemplos**

   - Backend:
     ```sh
     cp api/env.example api/.env
     ```

   - Frontend:
     ```sh
     cp web/env.example web/.env
     ```

3. **Suba a stack**
   ```sh
   docker compose up --build
   ```

4. **Acesse**
   - **Web (Streamlit)**: http://localhost:8501
   - **API (FastAPI)**: http://localhost:8000
   - **Ollama**: http://localhost:11434

## Baixar os modelos do Ollama (após subir o Docker Compose)

Com os containers em execução, abra um shell dentro do container `ollama` e faça o pull dos modelos usados pelo backend:

```sh
docker compose exec ollama sh
```

Dentro do container, rode:

```sh
ollama pull qwen3:1.7b
ollama pull nomic-embed-text
```

Depois, você pode sair do container:

```sh
exit
```

> Observação: os nomes dos modelos são configuráveis via `api/.env`:
> - `OLLAMA_CHAT_MODEL` (ex.: `qwen3:1.7b`)
> - `OLLAMA_EMBEDDING_MODEL` (ex.: `nomic-embed-text`)

Se você preferir sem entrar no shell interativo, também funciona assim:

```sh
docker compose exec ollama ollama pull qwen3:1.7b
docker compose exec ollama ollama pull nomic-embed-text
```

### Fontes de referência (obrigatórias para respostas)

As fontes curadas do MVP ficam em:

- `api/data/references/`

Adicione arquivos de referência `.txt` nessa pasta (curadoria interna). O assistente deve responder **somente** com evidências presentes nesses arquivos. (Ver `api/data/references/README.txt`)

> Importante: upload/gestão de fontes por usuários finais está **fora do escopo** do MVP.

## Prompts e desenvolvimento assistido por IA
Durante a construção do projeto, todos os **prompts utilizados no desenvolvimento assistido por IA** foram versionados e armazenados em:
- `prompts/`
Esses prompts serviram como guia e registro do processo, apoiando as principais fases do MVP:
- **Documentação inicial**: estruturação de **escopo** (`docs/escopo.md`), **backlog** (`docs/backlog.md`) e **arquitetura** (`docs/arquitetura.mmd`).
- **Desenvolvimento**: orientação de implementação do backend (API) e do frontend (UI), incluindo integrações e decisões de design.
- **Testes**: apoio na definição de estratégia e casos de teste automatizados.
- **Refatoração**: reorganização incremental do código e melhoria de manutenibilidade.
- **Documentação final**: consolidação de READMEs e instruções de uso/reprodução.
> Objetivo: garantir rastreabilidade do processo de construção (não apenas do código), facilitando manutenção, auditoria e evolução do MVP.

## Limitações (MVP)

- O chatbot **não** pode usar “conhecimento geral” não rastreável: se não houver evidência nas referências do MVP, ele deve **recusar**.
- O conjunto de fontes é **fixo e controlado pela equipe** (sem self-service de upload pelo usuário).
- Não substitui julgamento clínico: o objetivo é **consulta e validação** com rastreabilidade.
- Privacidade (LGPD): o usuário deve evitar inserir dados identificáveis de pacientes (o sistema é orientado a minimizar coleta).

## Próximos passos (sugestões)

- Pipeline formal de **ingestão e reindexação** (chunking, versionamento do índice e auditoria de mudanças).
- Melhorar guardrails de “modo confirmar análise” (ex.: checagens estruturadas e coleta de dados faltantes).
- Suporte a mais formatos de fonte (PDF/HTML com extração robusta) e melhor metadado (data de captura, seção/página).
- Autenticação mínima e controle de acesso (se necessário para ambiente real).
- Suite ampliada de testes com perguntas-alvo por fonte, para garantir cobertura e reduzir alucinação.
