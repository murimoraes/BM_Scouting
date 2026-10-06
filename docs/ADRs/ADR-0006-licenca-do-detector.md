# ADR-0006 — Licença do detector e dos modelos

- Status: **Proposta — aguarda decisão humana**
- Data da proposta: 2026-10-05
- Decisor(es): — | Data da decisão: —

## Contexto

A stack decidida cita "YOLO". A implementação mais popular (pacote `ultralytics`) é distribuída, até onde sabemos, sob
**AGPL-3.0**, com licença comercial ("Enterprise") vendida à parte — **verificar os termos vigentes no repositório e no site
oficiais antes de decidir**. A AGPL exige disponibilizar o código-fonte correspondente a usuários que interagem com o
software pela rede, o que conflita com um SaaS de código fechado. Trocar de detector depois de ajustar modelos e pipeline
custa retrabalho. "YOLO" é uma família: há implementações e arquiteturas de detecção sob licenças permissivas
(Apache-2.0/MIT) — cada uma com licença de **código e de pesos** a verificar individualmente.

Mesma questão vale para: leitor de número, ReID, modelos treinados com datasets não comerciais (RISKS R-12).

## Opções

**A. Ultralytics sob AGPL** e abrir o código do serviço.
**B. Ultralytics com licença comercial** (custo a cotar).
**C. Detector com licença permissiva** (código e pesos Apache-2.0/MIT), verificado item a item.
**D. Ultralytics apenas para experimento interno**, com migração antes do produto.

## Trade-offs

| Critério | A | B | C | D |
|---|---|---|---|---|
| Risco jurídico no SaaS | Baixo se cumprir AGPL; perde segredo do código | Baixo | Baixo (após verificação) | Alto se a migração não acontecer |
| Custo | 0 | Cotação | 0 | 0 agora, retrabalho depois |
| Conveniência/ecossistema | Alta | Alta | Média | Alta |
| Retrabalho | Nenhum | Nenhum | Nenhum | Certo |

## Recomendação

**C desde a Onda 1**: escolher o detector entre opções com licença permissiva verificada (código + pesos), comparando por
DET-1/DET-2 e OPS-1 no nosso GT. Se nenhuma atingir o alvo e o Ultralytics atingir (medido), reabrir a ADR para decidir
entre A e B com cotação em mãos. Evitar D: na prática a migração tende a não acontecer.

Regra geral proposta para o CLAUDE.md: **nenhuma dependência ou peso de modelo entra sem registro da licença** (nome,
versão, licença do código, licença dos pesos, dataset de treino e suas restrições) em um inventário a criar na Onda 1.

## O que nos faria mudar de ideia

- Parecer jurídico sobre AGPL em SaaS diferente do entendimento acima.
- Diferença de desempenho medida grande o bastante para justificar licença comercial.

## Decisão humana

_(preencher)_
