# Chat Farma API (FastAPI)

Backend do **Chat Farma (MVP)**. Esta API expõe um endpoint de chat que orquestra um fluxo **RAG (Retrieval-Augmented Generation)** para responder **exclusivamente** com base no acervo curado em `api/data/references`, retornando também **citações/trechos** para rastreabilidade.

## Tecnologias

- Python
- FastAPI
- Pytest (testes)
- Ollama (LLM e embeddings, normalmente via Docker)

## Pré-requisitos

- **Python 3.x**
- (Recomendado) **venv/virtualenv**
- Um servidor **Ollama** acessível (ex.: `http://localhost:11434`)
  - Se estiver rodando via Docker Compose na raiz do projeto, o Ollama já sobe junto.

## Configuração (.env)

1. Crie o `.env` a partir do exemplo:

```sh
cp env.example .env
```

2. Ajuste valores se necessário, em especial:

- `OLLAMA_BASE_URL` (ex.: `http://localhost:11434`)
- `OLLAMA_CHAT_MODEL` (ex.: `qwen3:1.7b`)
- `OLLAMA_EMBEDDING_MODEL` (ex.: `nomic-embed-text`)
- `RAG_REFERENCE_DIR` (padrão: `data/references`)

3. Para rodar o projeto usando docker, a url do ollama deve ser `http://ollama:11434`.

## Rodar localmente (Python)

A partir da pasta `api/`:

1. Crie e ative um ambiente virtual:

```sh
python -m venv .venv
```

Ativar no Windows (PowerShell):

```sh
.venv\Scripts\Activate.ps1
```

Ativar no Ubuntu:

```sh
source .venv/bin/activate
```

1. Instale dependências:

```sh
pip install -r requirements.txt
```

3. Suba a API:

```sh
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

A API ficará disponível em:

- http://localhost:8000

(Se habilitado pelo FastAPI) Documentação interativa:

- http://localhost:8000/docs

## Fontes de referência (RAG)

- Coloque/edite as fontes curadas em: `api/data/references/` (arquivos `.txt`).
- O MVP deve responder **somente** com evidências dessas fontes; caso não encontre suporte, deve **recusar**.

## Rodar os testes

A partir da pasta `api/` (com o venv ativado e dependências instaladas):

```sh
pytest
```

Opcional: ver cobertura (se estiver configurado no projeto/dependências):

```sh
pytest --cov=src --cov-report=term-missing
```

## Troubleshooting

- **Erro de conexão com Ollama**: verifique se o Ollama está rodando e se `OLLAMA_BASE_URL` aponta para o endereço correto.
- **Modelo não encontrado**: faça o pull dos modelos configurados em `OLLAMA_CHAT_MODEL` e `OLLAMA_EMBEDDING_MODEL` no Ollama.
