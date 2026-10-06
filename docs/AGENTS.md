# Agentes — papéis e regras de orquestração

O **Orquestrador** (sessão principal do Claude Code, supervisionada por Murilo ou pelo sócio) planeja, delega, integra e
responde pela síntese. Papéis abaixo podem ser executados pelo próprio Orquestrador ou por subagentes.

## Regras de orquestração

1. Delegar a subagente **somente** trilhas independentes (sem arquivos em comum) e de tamanho relevante.
   Tarefa pequena ou acoplada: o Orquestrador faz.
2. **Máximo de 3 subagentes simultâneos.**
3. Todo subagente recebe o briefing abaixo, completo. Briefing incompleto não é enviado.
4. **QA/Auditor é independente de quem implementou:** nunca audita o próprio trabalho; só aceita evidência de comando
   executado (saída de teste, `metrics.json` com `run_id`). Afirmação sem evidência = reprovada.
5. **Nenhum agente altera contratos JSON** (`docs/contracts/`) sem ADR e aprovação humana registrada na ADR.
6. Nenhum agente adiciona dependência, baixa dados/modelos ou acessa rede sem aprovação humana (ver CLAUDE.md).
7. Teste que falha duas vezes pelo mesmo motivo: parar e reportar diagnóstico ao Orquestrador.

### Modelo de briefing de subagente

```
Papel: <papel>
Objetivo: <uma frase>
Escopo de arquivos (pode escrever): <lista de caminhos>
Somente leitura: <lista>
Contrato de entrada: docs/contracts/v1/<x>.schema.json
Contrato de saída:   docs/contracts/v1/<y>.schema.json
Comando de verificação: <comando exato> → resultado esperado
Condição de parada: <quando parar e devolver>, incluindo "2 falhas pelo mesmo motivo"
Proibido: alterar contratos, adicionar dependências, acessar rede, tocar fora do escopo
Entrega: resumo + saída literal do comando de verificação
```

## Papéis

### Vision (detecção)
- **Missão:** detectar jogadores, goleiros, árbitros (Onda 1) e bola (Onda 3) com licença compatível com SaaS.
- **Entradas:** vídeo (via ingestão), config do detector.
- **Saídas:** `src/bm_scouting/detection/`, testes em `tests/detection/`, artefato `detections`.
- **Contrato:** consome metadados de vídeo (`header.video`); produz `detections` v1.
- **Pronto quando:** artefato valida; DET-1/DET-2 (DET-3 na Onda 3) medidos no GT com `run_id`; licença de código e
  pesos registrada (ADR-0006); OPS-1 da etapa medido.

### Tracking/ReID
- **Missão:** tracklets estáveis e reconexão conservadora (pureza > cobertura).
- **Entradas:** `detections`.
- **Saídas:** `src/bm_scouting/tracking/`, `tests/tracking/`, artefato `tracks`.
- **Contrato:** consome `detections` v1; produz `tracks` v1.
- **Pronto quando:** artefato valida; TRK-1 (antes/depois), TRK-3, TRK-4 medidos; cada `link` tem `method`.

### Identidade (número/time)
- **Missão:** rótulo de time por tracklet, votação de número por tracklet, candidatos ranqueados e confirmação de 1 clique.
- **Entradas:** `tracks`, recortes do vídeo, consulta (número + time).
- **Saídas:** `src/bm_scouting/identity/`, `tests/identity/`, artefato `player_identity`.
- **Contrato:** consome `tracks` v1; produz `player_identity` v1.
- **Pronto quando:** artefato valida; pipeline pausa em `pending_confirmation`; IDN-1..IDN-6 medidos; nenhum dado pessoal
  além de ID opaco em `confirmed_by`.

### Campo/Homografia
- **Missão:** homografia imagem→campo e posições em metros com qualidade por amostra.
- **Entradas:** `tracks`, `player_identity`, frames do vídeo.
- **Saídas:** `src/bm_scouting/field/`, `tests/field/`, artefato `field_positions`; relatório do spike 1.S em `docs/`.
- **Contrato:** consome `tracks` v1 e `player_identity` v1; produz `field_positions` v1.
- **Pronto quando:** artefato valida; FLD-1..FLD-4 medidos; amostras sem homografia válida marcadas, nunca inventadas.

### Eventos/Estatísticas
- **Missão:** eventos por regras geométricas versionadas e métricas consolidadas com confiabilidade.
- **Entradas:** `field_positions`, `events`.
- **Saídas:** `src/bm_scouting/events/`, `src/bm_scouting/stats/`, `tests/events/`, `tests/stats/`, artefatos `events`, `stats`.
- **Contrato:** consome `field_positions` v1; produz `events` v1 e `stats` v1.
- **Pronto quando:** artefatos validam; cada regra tem teste com cenário sintético; EVT-*, STA-1, STA-2 medidos.

### Relatório/LLM
- **Missão:** relatório útil que só afirma o que os dados sustentam.
- **Entradas:** `stats`, `events`, `player_identity`.
- **Saídas:** `src/bm_scouting/report/`, `tests/report/`, artefato `report_input`, texto do relatório, clipes.
- **Contrato:** consome `stats`, `events`, `player_identity` v1; produz `report_input` v1.
- **Pronto quando:** artefato valida; verificador automático garante REP-1 = 0 e REP-2 = 100 %; REP-3 avaliado por humanos.

### Backend/Infra
- **Missão:** orquestração, cache, ambiente reprodutível em GPU alugada e, na Onda 5, API/fila/worker/storage.
- **Entradas:** todos os contratos (validação), ADR-0004, ADR-0005.
- **Saídas:** `src/bm_scouting/pipeline/`, `tests/pipeline/`, procedimentos em `docs/`.
- **Contrato:** valida todos; não produz contrato de domínio.
- **Pronto quando:** G1.3 (cache 100 % em reexecução) evidenciado; OPS-1/OPS-2 medidos; nenhum dado em pasta sincronizada.

### QA/Auditor
- **Missão:** verificação independente; dono do GT, das métricas e dos relatórios de auditoria.
- **Entradas:** artefatos, GT, saídas de comandos.
- **Saídas:** `tests/` (testes de contrato e avaliação), `docs/EVALUATION.md`, `docs/audits/WAVE-<n>.md`.
- **Contrato:** valida todos contra schema e contra GT no mesmo formato.
- **Pronto quando:** gate da onda tem cada critério com PASSOU/FALHOU e evidência literal (comando + saída ou `run_id`);
  não auditou nada que ele mesmo implementou.

## Decisão de delegação nesta execução (Onda 0)

Nenhum subagente foi usado. Justificativa: os entregáveis são documentos fortemente acoplados (contratos ↔ métricas ↔
ADRs ↔ roadmap); dividir em trilhas paralelas aumentaria o risco de inconsistência sem ganho de tempo relevante.
