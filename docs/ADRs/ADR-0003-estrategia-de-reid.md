# ADR-0003 — Estratégia de ReID e reconexão de tracklets

- Status: **Proposta — aguarda decisão humana**
- Data da proposta: 2026-10-05
- Decisor(es): — | Data da decisão: —

## Contexto

ByteTrack associa por movimento/IoU e fragmenta identidades em 90 min (achado 4): oclusões em disputas, saídas de quadro,
falhas de detecção. Contrato afetado: `tracks` v1 (`links`, `global_id`).

Observação central: **companheiros de time vestem uniformes idênticos**. ReID genérico de pessoas (treinado para distinguir
roupas diferentes) tende a discriminar mal dentro do mesmo time. Por outro lado, o produto só exige identidade contínua do
**jogador-alvo**; para os demais basta o rótulo de time.

## Opções

**A. Sem aparência:** reconexão por restrições espaço-temporais (gap de tempo, velocidade máxima plausível, posição
prevista), mesmo time, e votos de número (ADR-0002) como evidência forte quando existirem.

**B. ReID genérico pré-treinado** (embeddings de pessoa) somado a A.

**C. ReID específico de futebol**, ajustado em dataset de esporte (ex.: tarefa de ReID da SoccerNet — licença a verificar).

**D. Aparência aprendida na própria partida** (ex.: embeddings ajustados online com pares positivos dos próprios tracklets).

**E. Revisão humana dos links do alvo** — mostrar ao usuário os pontos de reconexão de baixa confiança.

## Trade-offs

| Critério | A | B | C | D | E |
|---|---|---|---|---|---|
| Distingue companheiros de time | Só por posição/número | Fraco (hipótese a medir) | Melhor (hipótese) | Possivelmente melhor | Sim |
| Custo de GPU | ~0 | Médio | Médio | Alto | 0 |
| Dependência de dataset/licença | Nenhuma | Pesos públicos (verificar licença) | Dataset restrito provável | Nenhuma | Nenhuma |
| Dado biométrico (LGPD) | Não gera | Gera embeddings de aparência | Gera | Gera | Não |
| Complexidade | Baixa | Média | Alta | Alta | Baixa (técnica), custo de UX |

## Recomendação

**Escada medida, começando por A (+ E apenas para o alvo):**
1. Onda 1: A. Medir TRK-1 (antes/depois da reconexão), TRK-3 (pureza) e TRK-4 no GT.
2. Só se TRK-2/TRK-3 ficarem abaixo do alvo: experimentar B, comparando no mesmo GT; adotar apenas se a melhoria medida
   justificar custo de GPU e o tratamento LGPD dos embeddings.
3. C e D ficam para a Onda 6.
4. E é aplicado somente se a cobertura do alvo exigir, limitado a poucos pontos por partida (conta no IDN-4).

Regra de produto: na dúvida, **não conectar** (preferir lacuna a contaminação — pureza > cobertura).

## Consequências

- Embeddings de aparência, se adotados, são efêmeros: existem só durante o job, não são persistidos nem usados em outras
  partidas (evita base biométrica — RISKS R-10).
- `links.method` registra a origem de cada reconexão para auditoria.

## O que nos faria mudar de ideia

- Medição mostrando que A deixa TRK-2 muito abaixo do alvo mesmo com E.
- ReID genérico demonstrar, no nosso GT, separação boa dentro do mesmo time.

## Decisão humana

_(preencher)_
