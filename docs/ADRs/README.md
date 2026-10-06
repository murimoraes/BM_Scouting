# Architecture Decision Records

Uma ADR por decisão relevante ou irreversível. Mudança de contrato JSON **sempre** exige ADR.

| ADR | Decisão | Status | Bloqueia |
|---|---|---|---|
| [ADR-0001](ADR-0001-tipo-de-video-alvo.md) | Tipo de vídeo-alvo | **Proposta — aguarda decisão humana** | Início da Onda 1, GT, homografia |
| [ADR-0002](ADR-0002-estrategia-de-identidade.md) | Estratégia de identidade (votação por tracklet + 1 clique) | **Proposta — aguarda decisão humana** | Onda 1 fase 1.4 |
| [ADR-0003](ADR-0003-estrategia-de-reid.md) | Estratégia de ReID / reconexão | **Proposta — aguarda decisão humana** | Onda 1 fase 1.3 |
| [ADR-0004](ADR-0004-ambiente-de-execucao-gpu.md) | Localização de GPU / ambiente de execução | **Proposta — aguarda decisão humana** | Qualquer execução em GPU |
| [ADR-0005](ADR-0005-serializacao-artefatos.md) | Formato físico dos artefatos grandes | **Proposta — aguarda decisão humana** | Onda 1 fase 1.1 |
| [ADR-0006](ADR-0006-licenca-do-detector.md) | Licença do detector (AGPL vs. permissiva) | **Proposta — aguarda decisão humana** | Onda 1 fase 1.2 |

## Ciclo de vida

`Proposta` → `Aceita` (com nome do decisor e data) | `Rejeitada` | `Substituída por ADR-XXXX`.
Só humanos (Murilo ou sócio) mudam o status para `Aceita`. Agentes podem propor e revisar.

## Modelo

```markdown
# ADR-XXXX — Título
- Status: Proposta | Aceita | Rejeitada | Substituída por ADR-YYYY
- Data da proposta: AAAA-MM-DD
- Decisor(es): — | Data da decisão: —

## Contexto
## Opções
## Trade-offs
## Recomendação
## Consequências
## O que nos faria mudar de ideia
## Decisão humana (preenchido pelo decisor)
```
