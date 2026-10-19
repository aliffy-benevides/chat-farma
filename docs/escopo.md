# Escopo do MVP — Chat Farma

## 1. Visão geral
O **Chat Farma** é um MVP de chatbot para **consulta e confirmação de análises farmacoterapêuticas**, permitindo que profissionais de saúde (ex.: farmacêuticos clínicos) façam perguntas, interajam e recebam respostas **baseadas exclusivamente em fontes de referência** previamente definidas no desenvolvimento.

Neste MVP, o conjunto de fontes é **fixo e controlado pela equipe** (sites e textos carregados/curados durante o desenvolvimento). O **carregamento de novas “fontes de referência” por usuários** ficará para versões futuras.

## 2. Objetivo do MVP
- Entregar um chat funcional que:
  - Responda perguntas clínicas/farmacoterapêuticas **somente** com base no acervo de referência do MVP.
  - Apresente **citações/trechos** e **rastreabilidade** (de onde veio a informação).
  - Permita **confirmar** uma análise farmacoterapêutica com apoio das fontes (ex.: checagem de indicação, dose, ajuste renal, interações, efeitos adversos, monitoramento).

## 3. Premissas e restrições
- **Fontes de referência**: definidas pela equipe (curadoria interna) e disponíveis ao sistema via:
  - Conteúdo de sites previamente selecionados (capturados e indexados), e/ou
  - Textos/documentos (ex.: PDFs/HTML/TXT) carregados durante o desenvolvimento.
- O chat **não pode** responder com base em conhecimento “geral” não rastreável; deve **recusar** quando não houver evidência nas fontes.
- O MVP é orientado a **consulta** e **validação**. Não substitui julgamento clínico.

## 4. Personas e usuários-alvo
- **Profissional de saúde** (primário): farmacêutico clínico, residente, profissional de farmácia hospitalar/ambulatorial.

## 5. Requisitos funcionais (RF)

### RF-01 — Interface de chat
- O sistema deve oferecer uma interface de chat (web) para envio de mensagens e recebimento de respostas.

### RF-02 — Respostas baseadas exclusivamente em fontes
- O sistema deve gerar respostas **somente** a partir do acervo de referência disponível.
- Quando não houver suporte nas fontes, o sistema deve:
  - Informar que não encontrou evidência suficiente nas referências do MVP;
  - Sugerir reformulação da pergunta e/ou indicar quais termos buscar.

### RF-03 — Citações e rastreabilidade
- Cada resposta que contenha informação clínica deve incluir:
  - **Citações** (links/identificadores) das fontes usadas;
  - Preferencialmente **trechos** (snippets) relevantes.
- Deve ser possível identificar a fonte (ex.: título, URL, seção/página, data/captura quando aplicável).

### RF-04 — Consulta às fontes do MVP (busca e recuperação)
- O sistema deve:
  - Buscar conteúdo no acervo (indexado) por termos e similaridade semântica;
  - Recuperar trechos relevantes para compor a resposta.

### RF-05 — Modo “confirmar análise farmacoterapêutica”
- O sistema deve suportar perguntas e prompts voltados a **checagem/validação** de análises, com estrutura mínima:
  - Ex.: “Confirmar se dose X é adequada para ClCr Y”, “Interações entre A e B”, “Monitoramento recomendado para medicamento C”.
- O sistema deve responder com:
  - Conclusão condicional (quando aplicável),
  - Evidência/citações,
  - Limitações (quando faltarem dados do caso ou não houver fonte).

### RF-06 — Coleta de informações faltantes
- Quando a pergunta exigir dados clínicos não fornecidos (ex.: idade, peso, função renal, indicação), o sistema deve solicitar as informações mínimas necessárias antes de concluir.

### RF-07 — Política de segurança de resposta (guardrails)
- O sistema deve:
  - Evitar recomendações prescritivas fora do escopo das fontes;
  - Recusar instruções perigosas quando não suportadas;
  - Diferenciar informação geral (ex.: mecanismo) de decisão clínica (dose/conduta).


## 6. Requisitos não funcionais (RNF)

### RNF-01 — Confiabilidade e rastreabilidade
- Respostas devem ser **reprodutíveis** dado o mesmo conjunto de fontes e configuração.
- Cada resposta deve incluir rastreabilidade suficiente para auditoria.

### RNF-02 — Privacidade e conformidade (LGPD)
- O MVP deve:
  - Minimizar coleta de dados pessoais;
  - Orientar o usuário a não inserir dados identificáveis de pacientes.

### RNF-03 — Usabilidade
- UI simples, com:
  - Campo de texto e envio;
  - Seção de “Fontes usadas” por resposta;
  - Mensagens de erro claras quando não houver evidência.

### RNF-04 — Manutenibilidade
- Código modular (camadas: UI, orquestração, retrieval, geração).
- Cobertura de teste de no mínimo 80% do backend.
- Versionamento de fontes e do índice para rastrear mudanças.

## 7. Entregáveis do MVP
- Aplicação web de chat (frontend + backend).
- Mecanismo de recuperação com citações.
- Política de recusa quando não houver evidência.
- Documentação mínima:
  - Lista de fontes do MVP;
  - Política de uso e limitações;
  - Instruções de reindexação.

## 8. Critérios de aceite (alto nível)
- Dado um conjunto de perguntas de teste, o sistema:
  - Responde com citações válidas para perguntas cobertas pelas fontes;
  - Recusa adequadamente perguntas não cobertas;
  - Solicita dados adicionais quando necessário;

## 9. Fora de escopo (não incluído no MVP)
- Upload/gestão de fontes de referência por usuários finais (self-service).
- Integrações com prontuário eletrônico (EHR/PEP), sistemas hospitalares, ERPs.
- Autenticação/SSO avançado, perfis complexos e controle granular de permissões (além do mínimo necessário para o MVP).
- Suporte offline, app mobile nativo.
- Geração automática de relatórios formais assináveis, trilhas de auditoria completas e governança robusta.
- Atualização automática e contínua de sites (crawling recorrente em produção) além do processo interno de reindexação.
- Suporte multilíngue.
- Recomendações terapêuticas personalizadas sem dados clínicos suficientes ou sem respaldo nas fontes.

## 10. Riscos e mitigação (MVP)
- **Cobertura insuficiente das fontes** → mitigar com curadoria inicial e suíte de testes com perguntas-alvo.
- **Alucinação do modelo** → mitigar com RAG, citações obrigatórias e política de recusa.
- **Dados sensíveis no chat** → mitigar com avisos e instruções para não inserir dados identificáveis.
- **Conteúdo desatualizado** → mitigar com versionamento e data de captura nas citações.
