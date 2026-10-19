# Backlog (mínimo) — Chat Farma (MVP)

> Releases: **Core** → **Qualidade (testes)** → **Entrega final**

## Release 1 — Core (chat + RAG + guardrails)

### Épico: Fundamentos do produto
- [ ] **BL-CORE-01 — Definir stack e arquitetura mínima (UI, API, retrieval, geração)**
  - Critérios de aceite:
    - [ ] Repositório organizado em camadas: **UI**, **API/orquestração**, **retrieval/index**, **geração/resposta**.
    - [ ] Configuração por variáveis de ambiente (ex.: provider de LLM, caminhos do índice, modo debug).
    - [ ] Documentação curta em `README` explicando como rodar localmente.

- [ ] **BL-CORE-02 — Política de uso e aviso LGPD no chat**
  - Critérios de aceite:
    - [ ] UI exibe aviso: “não insira dados identificáveis de pacientes”.
    - [ ] Mensagens de aviso não bloqueiam uso, mas ficam visíveis e persistentes.

### Épico: Interface de chat (RF-01, RNF-03)
- [ ] **BL-CORE-03 — UI web de chat (MVP)**
  - Critérios de aceite:
    - [ ] Campo de texto + botão/enviar por Enter.
    - [ ] Histórico da conversa na sessão.
    - [ ] Estado de carregamento/erro (mensagem clara ao usuário).

- [ ] **BL-CORE-04 — Seção “Fontes usadas” por resposta**
  - Critérios de aceite:
    - [ ] Cada resposta renderiza lista de fontes (título/identificador + link/URL quando aplicável).
    - [ ] Se houver snippet, exibir trecho associado à fonte.
    - [ ] Quando não houver evidência, a seção de fontes aparece vazia e com mensagem “nenhuma fonte recuperada”.

### Épico: Backend de chat e contrato de resposta
- [ ] **BL-CORE-05 — Endpoint de chat (API) + streaming opcional**
  - Critérios de aceite:
    - [ ] Endpoint recebe: mensagem do usuário + contexto da conversa (mínimo viável).
    - [ ] Endpoint retorna: resposta + lista de citações + metadados (ex.: id do índice/versão).
    - [ ] Erros tratados sem vazar stack trace na UI.

- [ ] **BL-CORE-06 — Modelo de resposta “auditável” (schema)**
  - Critérios de aceite:
    - [ ] Resposta estruturada contém:
      - [ ] `answer` (texto final)
      - [ ] `citations[]` (id/título/url/seção/página/data_captura quando aplicável)
      - [ ] `snippets[]` (trechos com referência à citação)
      - [ ] `limitations` (quando aplicável)
      - [ ] `missing_information[]` (quando aplicável)
    - [ ] Resposta clínica **não** é emitida sem pelo menos 1 citação.

### Épico: Ingestão e indexação do acervo (RF-02, RF-04, RNF-01, RNF-04)
- [ ] **BL-CORE-07 — Pipeline de ingestão (fontes curadas pela equipe)**
  - Critérios de aceite:
    - [ ] Suporta ao menos 2 formatos: **HTML/TXT** e **PDF** (ou equivalente definido no projeto).
    - [ ] Extrai e persiste metadados: título, origem (URL/caminho), data de captura/carregamento.
    - [ ] Registra lista de fontes do MVP em arquivo versionado (ex.: `docs/fontes.md` ou `data/sources.json`).

- [ ] **BL-CORE-08 — Construção do índice de busca (lexical + semântica ou mínimo semântico)**
  - Critérios de aceite:
    - [ ] Processo de reindexação executável via comando (script/CLI).
    - [ ] Índice versionado (ex.: `index_version`) e referenciado na resposta.
    - [ ] Chunking com tamanho e overlap configuráveis.

- [ ] **BL-CORE-09 — Recuperação de trechos (retrieval) com top-k e filtros**
  - Critérios de aceite:
    - [ ] Busca retorna top-k trechos com score e metadados de fonte.
    - [ ] Permite ajustar `top_k` e limiar mínimo de relevância.
    - [ ] Retorno inclui trechos (snippets) diretamente exibíveis na UI.

### Épico: Geração de respostas restritas às fontes (RF-02, RF-03)
- [ ] **BL-CORE-10 — Prompting/orquestração “source-grounded” (RAG)**
  - Critérios de aceite:
    - [ ] Resposta final utiliza **apenas** o contexto recuperado.
    - [ ] Instrução explícita ao modelo: “se não houver evidência, recuse”.
    - [ ] Saída do modelo é pós-processada para garantir schema e citações.

- [ ] **BL-CORE-11 — Política de recusa quando não houver evidência**
  - Critérios de aceite:
    - [ ] Se retrieval retornar vazio ou abaixo do limiar, responder:
      - [ ] “não encontrei evidência suficiente nas referências do MVP”
      - [ ] sugestão de reformulação/termos para buscar.
    - [ ] Resposta não contém afirmações clínicas sem citação.

### Épico: Modo “confirmar análise farmacoterapêutica” (RF-05, RF-06)
- [ ] **BL-CORE-12 — Classificação de intenção: consulta vs. confirmação/validação**
  - Critérios de aceite:
    - [ ] Sistema identifica prompts de validação (dose, ajuste renal, interação, EA, monitoramento).
    - [ ] Para validação, ativa template de resposta com: conclusão condicional + evidência + limitações.

- [ ] **BL-CORE-13 — Coleta de informações faltantes**
  - Critérios de aceite:
    - [ ] Quando faltarem dados mínimos (ex.: ClCr, idade, peso, indicação), o sistema pergunta objetivamente.
    - [ ] `missing_information[]` é preenchido.
    - [ ] Não conclui dose/conduta sem os dados requeridos e sem evidência nas fontes.

### Épico: Guardrails de segurança (RF-07)
- [ ] **BL-CORE-14 — Regras de resposta segura e limites do MVP**
  - Critérios de aceite:
    - [ ] Diferencia conteúdo informativo vs. decisão clínica (ex.: não prescrever sem evidência).
    - [ ] Recusa instruções perigosas e solicita contexto clínico quando necessário.
    - [ ] Mensagem de limitação: “não substitui julgamento clínico”.

---

## Release 2 — Qualidade (testes, observabilidade mínima, reprodutibilidade)

### Épico: Testes e cobertura (RNF-04)
- [ ] **BL-QUAL-01 — Suíte de testes automatizados do backend (≥ 80%)**
  - Critérios de aceite:
    - [ ] Cobertura ≥ 80% (relatório gerado em CI/local).
    - [ ] Testes unitários para: chunking, index versioning, schema de resposta, política de recusa.
    - [ ] Testes de integração para: pipeline retrieval → geração → resposta com citações.

- [ ] **BL-QUAL-02 — Conjunto de perguntas-alvo (golden set) e testes de regressão**
  - Critérios de aceite:
    - [ ] Arquivo versionado com perguntas e expectativas mínimas.
    - [ ] Para perguntas cobertas: teste valida **existência** e **formato** de citações.
    - [ ] Para perguntas não cobertas: teste valida recusa.

### Épico: Observabilidade mínima e rastreabilidade (RNF-01)
- [ ] **BL-QUAL-03 — Logging estruturado e correlação por requisição**
  - Critérios de aceite:
    - [ ] Logs incluem request_id, index_version, top_k, ids das fontes recuperadas.
    - [ ] Logs não armazenam dados pessoais; incluir aviso no código/README.

- [ ] **BL-QUAL-04 — Persistência mínima de auditoria (opcional no MVP, mas recomendada)**
  - Critérios de aceite:
    - [ ] Armazena: pergunta, resposta, citations, index_version, timestamp (sem PII).
    - [ ] Pode ser desativado por configuração.

---

## Release 3 — Entrega final (hardening, docs, UX e operação)

### Épico: Documentação e operação (Entregáveis do MVP)
- [ ] **BL-FINAL-01 — Documentar “Lista de fontes do MVP” e versão do índice**
  - Critérios de aceite:
    - [ ] Documento lista fontes com título + URL/caminho + data de captura.
    - [ ] Processo de atualização/reindexação descrito (passo a passo).

- [ ] **BL-FINAL-02 — Documentar política de uso e limitações (inclui recusa)**
  - Critérios de aceite:
    - [ ] Explica: escopo, o que o sistema faz/não faz, como interpretar citações.
    - [ ] Inclui exemplos de perguntas boas/ruins.

### Épico: UX e robustez
- [ ] **BL-FINAL-03 — Tratamento de erros e estados vazios na UI**
  - Critérios de aceite:
    - [ ] Mensagens amigáveis para: falha no backend, timeout, sem evidência.
    - [ ] Botão para “copiar resposta” e “copiar fontes” (opcional, se couber no MVP).

- [ ] **BL-FINAL-04 — Sanitização e limites de entrada**
  - Critérios de aceite:
    - [ ] Limite de tamanho de mensagem.
    - [ ] Bloqueio/alerta para padrões de PII simples (ex.: CPF, telefone) com orientação.

### Épico: Empacotamento e deploy
- [ ] **BL-FINAL-05 — Deploy mínimo (ambiente único) + instruções**
  - Critérios de aceite:
    - [ ] Build e execução documentados.
    - [ ] Variáveis de ambiente listadas e explicadas.
    - [ ] Checklist de smoke test pós-deploy.

### Épico: Critérios de aceite do MVP (alto nível)
- [ ] **BL-FINAL-06 — Execução da bateria de aceite (manual + automatizada)**
  - Critérios de aceite:
    - [ ] Perguntas cobertas retornam respostas com citações válidas.
    - [ ] Perguntas não cobertas são recusadas adequadamente.
    - [ ] Perguntas que requerem dados adicionais acionam coleta de informações faltantes.
