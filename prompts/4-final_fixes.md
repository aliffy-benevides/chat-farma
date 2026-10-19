# 1. Reinforce chat response when there is no source to support answer
Contexto: @escopo.md e @CurrentFile .

Execute as seguintes alterações em ordem:

- Exclua hits e faça a função answer_with_context esperar no formato de sources

- Antes de iterar sobre os docs, verifique se tem fontes válidas (docs)

- Caso não existir, envie outra resposta formulada pela LLM, dizendo "que não foi possível encontrar {pergunta do usuário}".

# 2. Mock Ollama on tests

Contexto: Leia os testes em api/tests, busque por testes que dependem da LLM indiretamente.

Objetivo: Aplique mocks antes da criação da aplicação e da indexação para não depender do Ollama real.

## 2.1 Mock OllamaEmbeddings

Reforce que *NÃO* será necessário o ollama rodando para executar os testes da api, mock todos os pontos que interagem com o ollama, inclusive os pontos que o agent interage com a LLM e em que o rag utiliza o Embeddings.

## 2.2 Mock OllamaEmbeddings - segunda tentativa

embeddings = OllamaEmbeddings(
    model=os.getenv("OLLAMA_EMBEDDING_MODEL", "nomic-embed-text"),
    base_url=os.getenv("OLLAMA_BASE_URL", "http://localhost:11434"),
)

Mock o OllamaEmbeddings nos testes do rag.

## 2.3 Mock OllamaEmbeddings - passando o erro

.venv/lib/python3.14/site-packages/langchain_community/vectorstores/faiss.py:1043: AttributeError

======================================================= short test summary info ========================================================

ERROR tests/test_main.py::test_health_success - AttributeError: 'FakeEmbeddings' object has no attribute 'embed_documents'

## 2.3 Mock OllamaEmbeddings - erro após ajustes manuais

.venv/lib/python3.14/site-packages/langchain_community/vectorstores/faiss.py:1001: TypeError

======================================================= short test summary info ========================================================

ERROR tests/test_main.py::test_health_success - TypeError: 'NoneType' object is not subscriptable
