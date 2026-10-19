# Chat Farma Web (Frontend)

Frontend do **Chat Farma (MVP)**. Esta aplicação fornece uma **interface de chat** para profissionais de saúde enviarem perguntas clínicas/farmacoterapêuticas e receberem respostas da **Chat Farma API**, incluindo **fontes/citações** quando disponíveis.

O frontend **não gera respostas por conta própria**: ele apenas envia mensagens para a API e renderiza a resposta, histórico e seção de fontes.

## Tecnologias

- Python
- Streamlit
- Client HTTP para integração com a API

## Pré-requisitos

- **Python 3.x**
- (Recomendado) **venv/virtualenv**
- **Chat Farma API** rodando e acessível (ex.: `http://localhost:8000`)

## Configuração (.env)

1. Crie o `.env` a partir do exemplo (na pasta `web/`):

```sh
cp env.example .env
```

2. Principais variáveis:

- `CHATFARMA_API_URL`  
  URL base da API FastAPI (ex.: `http://localhost:8000` ou `http://api:8000` para docker)

- `CHATFARMA_HTTP_TIMEOUT`  
  Timeout (segundos) para chamadas HTTP (ex.: `60`)

## Rodar localmente (Python)

A partir da pasta `web/`:

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

2. Instale dependências:

```sh
pip install -r requirements.txt
```

3. Suba o Streamlit:

```sh
streamlit run app.py
```

A UI ficará disponível em:

- http://localhost:8501

## Como usar (básico)

1. Garanta que a **API esteja rodando** e que `CHATFARMA_API_URL` no `web/.env` aponte para ela.
2. Abra o frontend em `http://localhost:8501`.
3. Digite sua pergunta no chat e envie.
4. Confira na resposta:
   - O texto retornado pela API
   - A seção de **fontes/citações** (quando a resposta estiver suportada pelo acervo do MVP)
5. Se a API indicar falta de evidência nas fontes, reformule a pergunta com termos mais específicos (ex.: nome do fármaco, condição, dose, via, ajuste renal, etc.).

## Observações e limitações (MVP)

- Evite inserir dados identificáveis de pacientes (LGPD).
- Se a API recusar por falta de evidência no acervo curado, o frontend apenas exibirá a recusa e sugestões retornadas.
