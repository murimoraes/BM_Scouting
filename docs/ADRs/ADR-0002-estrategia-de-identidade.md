# ADR-0002 — Estratégia de identidade do jogador-alvo

- Status: **Proposta — aguarda decisão humana**
- Data da proposta: 2026-10-05
- Decisor(es): — | Data da decisão: —

## Contexto

Entrada do usuário: número da camisa + time. O número raramente está legível (achado 3): costas viradas para a câmera,
baixa resolução, oclusão, borrão de movimento. Errar a identidade invalida o relatório inteiro — é o erro mais caro do
produto. Contrato afetado: `player_identity` v1.

## Opções

**A. Leitura de número por frame (OCR/STR/VLM), sem agregação.** Identidade = frames onde o número foi lido.

**B. Votação por tracklet + confirmação humana de 1 clique.**
1. Time por agrupamento de cor do tronco (não supervisionado, por partida) → `team_assignment`.
2. Filtro de legibilidade (recorte grande o suficiente, costas/frente visíveis) antes de ler o número.
3. Leitura do número nos recortes legíveis; votos agregados por tracklet (`jersey_observations`).
4. Tracklets do time pedido, ranqueados por votos no número pedido + continuidade (`candidates`).
5. Usuário vê miniaturas dos 3 primeiros candidatos (frames de evidência) e confirma com 1 clique, ou corrige clicando
   no jogador em um frame (`selection`).

**C. Seleção totalmente manual.** Usuário clica no jogador em um frame; sem leitura de número.

**D. Auto-aceite sem humano** quando a confiança passar de um limiar.

## Trade-offs

| Critério | A | B | C | D |
|---|---|---|---|---|
| Robustez a número ilegível | Baixa | Média–alta (agrega e cai para o humano) | Alta | Baixa–média |
| Esforço do usuário | 0 | ~1 clique (meta IDN-4 ≤ 5 interações) | Alguns cliques + risco de clicar errado | 0 |
| Risco de relatório do jogador errado | Alto | Baixo (humano confirma com evidência) | Baixo | Médio |
| Custo de GPU | Alto (todos os frames) | Médio (só recortes legíveis) | Mínimo | Médio |
| Escala para SaaS | Sim | Sim (1 clique cabe em fluxo assíncrono) | Sim | Sim |

## Recomendação

**B, com C como fallback dentro do mesmo fluxo** (se nenhum candidato estiver certo, o usuário clica no jogador → método
`human_correction`). **D proibido no MVP**: `auto_accepted` fica no contrato para uso futuro, só habilitável após IDN-2
medido no holdout acima de um limiar aprovado por ADR.

Detalhes que esta ADR fixa:
- O pipeline **pausa** após `identity` com `selection.status = pending_confirmation`; etapas a jusante só rodam com
  `confirmed` ou `corrected`.
- `confirmed_by` é ID opaco do usuário (nunca nome/e-mail).
- O modelo de leitura de número **não** é escolhido aqui: candidatos (modelos de reconhecimento de texto em cena, VLMs)
  serão comparados na Onda 1 por IDN-6, custo (OPS-1) e licença (ADR-0006).

## Consequências

- Etapa humana síncrona na Onda 1 (CLI mostra miniaturas/arquivos de imagem e pede o número do candidato).
- Na Onda 5 a etapa vira notificação + tela; o job fica em estado "aguardando confirmação".
- Recortes de rosto/corpo usados como evidência são dado pessoal: retenção curta, não reutilizar para treino sem base legal.

## O que nos faria mudar de ideia

- IDN-3 (top-3) medido muito abaixo do alvo → investir em ReID por aparência (ADR-0003) ou em seleção manual (C) como padrão.
- Usuários recusarem qualquer passo manual (validação de produto).

## Decisão humana

_(preencher)_
