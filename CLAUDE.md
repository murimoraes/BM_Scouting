# BM Scouting — instruções para Claude Code

SaaS em Python: vídeo de partida + número da camisa + time → relatório individual do jogador.
Equipe: Murilo + sócio. Documentação em pt-BR; identificadores de código e chaves JSON em inglês.

**Estado atual:** Onda 0 (fundação) entregue; Onda 1 bloqueada por decisões humanas — ver
[docs/ROADMAP.md](docs/ROADMAP.md) e [docs/ADRs/README.md](docs/ADRs/README.md).

## Regra nº 1 — evidência antes de afirmação

- Não diga que algo "funciona", "passou", "melhorou" ou "está pronto" sem ter executado o comando e mostrado a saída
  real (ou o `run_id` com `data/runs/<run_id>/metrics.json`).
- Todo número em documento ou resposta é: **medido** (com comando/arquivo), **citado** (com fonte) ou marcado
  **"estimativa a validar"**. Valores-alvo são "a calibrar com dados reais" até serem medidos no holdout.
- Falhou o mesmo teste duas vezes pelo mesmo motivo: pare e reporte o diagnóstico; não tente uma terceira correção às cegas.
- Ao concluir um entregável, reporte: `✅ [o que] — [arquivo(s)] — [comando de verificação e resultado real]`.

## Comandos

```bash
python -m pytest                              # suíte completa
python -m pytest tests/test_contracts.py -v   # só contratos JSON
make test                                     # equivalente, se houver make (no Windows normalmente não há)
python -m pip install -e ".[dev]"             # instala pytest + jsonschema (acessa a rede)
```

Requer Python ≥ 3.11. O `pytest` já adiciona `src/` ao path (ver `pyproject.toml`); instalar o pacote é opcional.

## Estrutura

```
CLAUDE.md                 este arquivo
docs/ROADMAP.md           ondas, fases, gates
docs/ARCHITECTURE.md      pipeline, cache, coordenadas
docs/AGENTS.md            papéis, briefing de subagente
docs/EVALUATION.md        métricas, protocolo de ground truth
docs/COST_MODEL.md        custo por partida e mensal
docs/RISKS.md             registro de riscos
docs/ADRs/                decisões (status, opções, recomendação)
docs/contracts/v1/        JSON Schemas + examples/
docs/audits/              relatório de auditoria por onda
src/bm_scouting/<módulo>/ detection, tracking, identity, field, events, stats, report, pipeline
tests/                    pytest
```

## Convenções

- **Módulos só conversam por artefato JSON** que valida contra `docs/contracts/v1/`. Proibido importar código interno de
  outro módulo de domínio.
- Todo artefato tem `header` com `inputs` (hashes) — base da chave de cache (ARCHITECTURE §3). Ao mudar comportamento de
  um módulo, incremente `module_version`.
- Valor não calculável = `null` + `reliability: "unavailable"`. Nunca preencher com estimativa silenciosa.
- Coordenadas: pixels da resolução original (origem superior esquerda) ou metros no sistema de `field_positions`.
- Testes com pytest; cada módulo novo vem com testes e com o comando de verificação no relatório.

## Regras de escopo

- Trabalhe **somente na onda/fase corrente** do ROADMAP. Não antecipe funcionalidades, refatorações ou abstrações.
- **Contratos JSON:** qualquer mudança exige ADR + aprovação humana registrada + bump de versão + exemplo atualizado +
  `python -m pytest tests/test_contracts.py` passando.
- **Peça aprovação humana antes de:** deletar arquivos; adicionar dependência (registrar licença de código e de pesos —
  ADR-0006); baixar datasets, vídeos ou pesos; acessar a rede; criar arquivos fora de `CLAUDE.md`, `docs/`, `src/`,
  `tests/`, `pyproject.toml`, `Makefile` (ex.: `.gitignore`, `Dockerfile`, `data/`); executar em GPU alugada.
- **Dados:** vídeos, frames, recortes, embeddings e GT ficam em `data/` (fora do git e **fora de pasta sincronizada**,
  ver RISKS R-15). Nunca commitar dado pessoal. Nunca usar vídeo com menores sem consentimento registrado (R-11).
- Decisões abertas (ADRs com status "Proposta") **não** são decididas por agente: apresente e aguarde o humano.

## Subagentes

Ver [docs/AGENTS.md](docs/AGENTS.md): no máximo 3 simultâneos, só trilhas independentes, briefing completo, QA
independente de quem implementou.
