# ADR-0001 — Tipo de vídeo-alvo do MVP

- Status: **Proposta — aguarda decisão humana**
- Data da proposta: 2026-10-05
- Decisor(es): — | Data da decisão: —

## Contexto

O tipo de vídeo decide a viabilidade técnica de quase todas as etapas (homografia, visibilidade do alvo, leitura de
número), o mercado e o risco jurídico. É a decisão de maior impacto do projeto e ainda está aberta (achado de auditoria 2).
O GT (EVALUATION §3) só pode ser coletado depois dela.

## Opções

**A. Transmissão de TV** — câmera principal com pan/zoom, cortes, replays, closes, gráficos sobrepostos.

**B. Câmera tática fixa / panorâmica** — câmera elevada e estática (ou sistema panorâmico) que enquadra o campo inteiro
o tempo todo. Inclui exportações panorâmicas de sistemas automáticos de filmagem, quando o arquivo panorâmico bruto estiver
disponível (a verificar por fornecedor).

**C. Amador / mão** — celular ou filmadora operada na arquibancada, com pan/zoom manual e tremor.

**D. Vários tipos desde o início.**

## Trade-offs

| Critério | A. TV | B. Fixa/panorâmica | C. Amador | D. Todos |
|---|---|---|---|---|
| Homografia | Difícil: dinâmica, por frame, cortes e replays (pesquisa — achado 1) | Mais fácil: estática ou quase; calibrar uma vez por partida | Difícil: dinâmica + tremor + enquadramento parcial | Soma das dificuldades |
| Alvo em quadro | Parcial: jogador sai de quadro com frequência; 90 min de trajetória individual não existem | Sempre em quadro (salvo oclusão) | Parcial e imprevisível | — |
| Leitura de número | Melhor (jogadores maiores, closes) | Pior (jogadores pequenos em pixels) → depende mais do 1 clique | Variável | — |
| Distância/mapa de calor | Incompleto por construção | Completo | Incompleto | — |
| Direitos do vídeo | Alto risco: direitos de transmissão pertencem a terceiros | Menor: geralmente do clube/escolinha que filmou | Menor, mas autoria difusa | — |
| Mercado provável (hipótese a validar) | Scouts e agentes analisando atletas profissionais | Clubes amadores, categorias de base, escolinhas, academias | Pais, atletas amadores | — |
| Menores de idade | Baixo (profissional) | **Alto** (base) → LGPD art. 14 | Alto | — |
| Complexidade p/ 2 pessoas | Alta | Média | Alta | Inviável no MVP |

## Recomendação

**B — câmera tática fixa/panorâmica**, com especificação mínima de entrada a validar com vídeos reais:
campo inteiro visível, câmera elevada e estática, resolução ≥ 1080p, sem cortes de edição. Vídeos fora da especificação
são recusados na ingestão (com mensagem ao usuário), não processados com qualidade degradada silenciosa.

Justificativa: é a única opção em que as saídas centrais do produto (trajetória, mapa de calor, distância) são
**completas por construção** e a homografia deixa de ser risco de pesquisa. A fraqueza (número pouco legível) é
mitigada pela confirmação de 1 clique (ADR-0002), que já é necessária em qualquer opção.

Custo da recomendação: o mercado de B concentra categorias de base → menores de idade → obrigações LGPD reforçadas
(RISKS R-11) desde o início. Isso precisa ser aceito conscientemente junto com esta ADR.

A pode virar uma 2ª linha de produto (Onda 6) se houver demanda e solução de direitos.

## Consequências

- GT: 3 partidas de câmera fixa, com autorização do clube.
- Onda 2: homografia estática/keyframes primeiro; dinâmica só se necessária.
- É preciso **obter vídeos de amostra** do tipo B antes da Onda 1 — ação humana (contato com clubes/escolinhas).

## O que nos faria mudar de ideia

- Validação de mercado mostrar que os clientes pagantes só têm vídeo de TV.
- Vídeos do tipo B disponíveis terem resolução tão baixa que nem detecção de jogador (DET-1) atinja o alvo.
- Impossibilidade prática de cumprir LGPD para menores no público de B.

## Decisão humana

_(preencher: opção escolhida, especificação mínima de vídeo aceita, decisor, data)_
