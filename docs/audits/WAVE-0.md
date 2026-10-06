# Auditoria — Onda 0 (Fundação)

- Data: 2026-10-05
- Auditor: Orquestrador (autoauditoria — **limitação**: o papel QA/Auditor deveria ser independente; recomenda-se que o
  sócio revise este relatório e reexecute os comandos abaixo antes de aceitar o gate).

## Evidência

| Comando | Resultado real |
|---|---|
| `python -m pytest -q` | `61 passed in 0.51s` |
| Verificação de links relativos em todos os `.md` | `quebrados: 0` |
| `grep -rnE "^\s*(import\|from) " src` | nenhum import em `src/` (sem código de ML) |
| Checagem de seções nas ADRs 0001–0006 | Opções, Trade-offs, Recomendação, Status "Proposta" presentes em todas |

Os 61 testes: 8 meta-schema, 1 cobertura de schemas, 7 `$id`, 7 exemplos válidos, 7 `schema_name` do header,
7 rejeições de campo extra, 16 rejeições de mutação inválida, 8 imports do esqueleto.

## Gate de saída

| Critério | Resultado | Evidência |
|---|---|---|
| G0.1 Todos os entregáveis existem | PASSOU | listagem de arquivos (`find`) |
| G0.2 `python -m pytest` passa | PASSOU | `61 passed` |
| G0.3 Cada contrato tem schema versionado + exemplo | PASSOU | `test_every_artifact_has_schema`, `test_example_is_valid[*]` |
| G0.4 Cada etapa tem métrica com alvo "a calibrar" | PASSOU | EVALUATION §2.1–2.7 (regra geral + legenda por seção) |
| G0.5 ADRs obrigatórias 0001–0004 completas | PASSOU | checagem de seções |
| G0.6 Sem código de ML; nada baixado | PASSOU | grep sem imports; nenhum download executado |
| G0.7 Nenhum número de desempenho apresentado como medido | PASSOU (revisão manual) | números são alvos "a calibrar", estimativas marcadas ou limites citados (IFAB Lei 1) |

## Itens fora do escopo de arquivos, pendentes de aprovação

- `.gitignore` (excluir `data/`, caches) e `git init` — R-16.
- Mover o projeto para fora do OneDrive organizacional — R-15.
- `.pytest_cache/` e `__pycache__/` foram gerados pela execução dos testes; não foram removidos (remoção exige aprovação).
