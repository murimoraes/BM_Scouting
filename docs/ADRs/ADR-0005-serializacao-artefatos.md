# ADR-0005 — Formato físico dos artefatos grandes

- Status: **Proposta — aguarda decisão humana**
- Data da proposta: 2026-10-05
- Decisor(es): — | Data da decisão: —

## Contexto

Os contratos são JSON Schema. `detections`, `tracks` e `field_positions` têm uma entrada por frame processado; para
90 min a dezenas de fps com ~25 pessoas por frame, o JSON pode ficar na casa de centenas de MB (ordem de grandeza
**estimada, não medida**). Isso afeta cache, tempo de leitura e custo de storage.

## Opções

**A. JSON puro** (`.json`).
**B. JSON comprimido** (`.json.gz`) — mesmo schema, validação idêntica após descompressão.
**C. JSON Lines por frame** — exige schema separado por linha; muda a forma do contrato.
**D. Parquet/Arrow** para as partes tabulares + JSON para cabeçalho — compacto e rápido, nova dependência, validação via
schema próprio.

## Trade-offs

| Critério | A | B | C | D |
|---|---|---|---|---|
| Mudança de contrato | Nenhuma | Nenhuma | Sim (MAJOR) | Sim (MAJOR) |
| Tamanho em disco | Grande | Menor | Grande | Menor |
| Streaming/leitura parcial | Não | Não | Sim | Sim |
| Dependências novas | Não | Não (gzip é stdlib) | Não | Sim |

## Recomendação

**B na Onda 1**, medindo tamanho e tempo de leitura/gravação de uma partida real (registrar no relatório da Onda 1).
Reabrir esta ADR para D apenas se a medição mostrar gargalo real (definir limiar na própria medição).
A extensão do arquivo não altera o schema lógico; o validador descomprime antes de validar.

## O que nos faria mudar de ideia

Medição da Onda 1 mostrando leitura/gravação dominando o tempo de etapas leves ou estourando memória do worker.

## Decisão humana

_(preencher)_
