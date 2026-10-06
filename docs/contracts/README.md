# Contratos JSON entre módulos

Os contratos são a **única** interface entre módulos (ver [ARCHITECTURE.md](../ARCHITECTURE.md)).
Todo artefato produzido pelo pipeline deve validar contra o schema correspondente.

| Artefato | Schema | Produzido por | Consumido por | Onda |
|---|---|---|---|---|
| `detections` | [v1/detections.schema.json](v1/detections.schema.json) | detection | tracking | 1 |
| `tracks` | [v1/tracks.schema.json](v1/tracks.schema.json) | tracking | identity, field | 1 |
| `player_identity` | [v1/player_identity.schema.json](v1/player_identity.schema.json) | identity (+ confirmação humana) | field, stats, report | 1 |
| `field_positions` | [v1/field_positions.schema.json](v1/field_positions.schema.json) | field | events, stats | 2 |
| `events` | [v1/events.schema.json](v1/events.schema.json) | events | stats, report | 3 |
| `stats` | [v1/stats.schema.json](v1/stats.schema.json) | stats | report | 2–4 |
| `report_input` | [v1/report_input.schema.json](v1/report_input.schema.json) | report | LLM | 4 |

Definições compartilhadas (header, bbox, ponto, hash etc.) ficam em [v1/common.schema.json](v1/common.schema.json).
Exemplos mínimos válidos ficam em [v1/examples/](v1/examples/). **Todos os valores dos exemplos são fictícios**
(hashes, métricas, coordenadas); não representam desempenho de nada.

## Convenções

- JSON Schema draft 2020-12. Chaves em inglês, `snake_case`.
- `additionalProperties: false` em todos os objetos: campo desconhecido é erro (pega erro de digitação e mudança não registrada).
- Todo artefato começa com `header` (nome e versão do schema, partida, vídeo, produtor, entradas). `header.inputs` lista os
  hashes dos artefatos de entrada: é a linhagem e a base da chave de cache.
- Pixels: resolução original do vídeo, origem no canto superior esquerdo. Metros: sistema do campo definido em `field_positions`.
- Tempo: `frame_index` (base 0) é a referência; `timestamp_s` é derivado.
- Valores que não puderam ser calculados são `null` com `reliability: "unavailable"` — nunca um número inventado.
- Dados pessoais: `match_id` é opaco; nome do jogador só em `report_input.player.display_name`, opcional (LGPD, ver RISKS.md).
- Ground truth anotado manualmente usa os **mesmos** contratos com `producer.module = "human_annotation"`.

## Versionamento

- `MAJOR` = diretório (`v1/`). `header.schema_version` = `1.MINOR.PATCH`.
- PATCH: descrição/documentação, sem efeito de validação.
- MINOR: campo novo **opcional** ou enum ampliado. Exige atualizar exemplo.
- MAJOR: qualquer mudança que invalide artefatos existentes → novo diretório `v2/`, `v1/` permanece até migração.
- **Qualquer** mudança de contrato exige: ADR em `docs/ADRs/`, aprovação humana registrada na ADR, exemplo atualizado e
  `python -m pytest tests/test_contracts.py` passando. Nenhum agente altera contrato sem isso.

## Verificação

```bash
python -m pytest tests/test_contracts.py -v
```

O teste checa meta-schema, existência de exemplo por contrato, validade dos exemplos e rejeição de mutações inválidas
conhecidas. Os `$ref` são resolvidos por um `Registry` local; o domínio `bmscouting.invalid` (reservado, RFC 2606) nunca é
acessado pela rede.

## Questão aberta

Artefatos por frame (`detections`, `tracks`, `field_positions`) de 90 min podem ficar grandes em JSON puro.
Formato físico em disco está na [ADR-0005](../ADRs/ADR-0005-serializacao-artefatos.md); o schema lógico não muda.
