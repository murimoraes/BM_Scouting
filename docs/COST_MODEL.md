# Modelo de custo

> Tudo aqui é **estimativa a validar**. Nenhum valor foi medido. Os preços de GPU são **ilustrativos** para formar
> cenários — consultar os preços vigentes do provedor escolhido (ADR-0004) e substituir na tabela de premissas.
> A primeira medição real (OPS-1) acontece na Onda 1.

## 1. Premissas editáveis

Edite a coluna "Base" e recalcule com as fórmulas da §2.

| ID | Premissa | Otimista | Base | Pessimista | Origem |
|---|---|---|---|---|---|
| P1 | Minutos de vídeo processados por partida (`D`) | 95 | 95 | 95 | Estimativa: 90 min + acréscimos; intervalo descartado na ingestão |
| P2 | Razão GPU-min por min de vídeo (`r`), todas as etapas GPU somadas | 0,5 | 1,0 | 2,0 | **Desconhecida** — cenários; medir na Onda 1 (OPS-1) |
| P3 | Overhead por job em GPU: subir máquina, carregar modelos, transferir vídeo (`o`, min) | 5 | 10 | 15 | Estimativa |
| P4 | Preço da GPU (`p`, US$/h) | 0,30 | 0,70 | 2,00 | **Ilustrativo** — substituir por preço vigente |
| P5 | Fator de reprocessamento (falhas, reexecuções) (`k`) | 1,1 | 1,2 | 1,5 | Estimativa |
| P6 | Tamanho do vídeo por partida (GB) | 1 | 2 | 4 | Estimativa (depende de resolução/bitrate) |
| P7 | Preço de storage (US$/GB-mês) | `s` | `s` | `s` | A preencher com o provedor |
| P8 | Retenção do vídeo (meses) | 0,25 | 1 | 3 | Decisão de produto/LGPD (minimizar) |
| P9 | Custo do LLM por relatório (US$) | `c_llm` | `c_llm` | `c_llm` | A preencher: tokens de entrada/saída × preço vigente do modelo escolhido |
| P10 | Custo fixo mensal (servidor web, fila, domínio, monitoramento) (`F`, US$) | `F` | `F` | `F` | A preencher na Onda 5 |
| P11 | Partidas por mês (`N`) | 10 | 50 | 200 | Cenários de volume |
| P12 | Minutos humanos por partida (confirmação + revisão) (`h`) | — | — | — | Medir (IDN-4); custo de mão de obra, não de nuvem |

Alavancas que mudam `r` (P2): passo de frames processados (`frame_stride`), resolução de entrada, tamanho do modelo,
leitura de número só em recortes legíveis, homografia estática (câmera fixa) vs. por frame.

## 2. Fórmulas

```
horas_gpu_partida   = (D × r + o) / 60
custo_gpu_partida   = horas_gpu_partida × p × k
custo_storage_part. = tamanho_GB × s × retenção_meses
custo_partida       = custo_gpu_partida + custo_storage_part. + c_llm
custo_mensal        = N × custo_partida + F
```

## 3. Cenários — somente GPU (calculado com as premissas acima)

| Cenário | horas_gpu_partida | custo_gpu_partida |
|---|---|---|
| Otimista: (95×0,5 + 5)/60 × 0,30 × 1,1 | 0,875 h | **US$ 0,29** |
| Base: (95×1,0 + 10)/60 × 0,70 × 1,2 | 1,75 h | **US$ 1,47** |
| Pessimista: (95×2,0 + 15)/60 × 2,00 × 1,5 | 3,42 h | **US$ 10,25** |

Custo mensal de GPU (`N × custo_gpu_partida`, sem storage, LLM e fixo):

| N partidas/mês | Otimista | Base | Pessimista |
|---|---|---|---|
| 10 | US$ 2,89 | US$ 14,70 | US$ 102,50 |
| 50 | US$ 14,44 | US$ 73,50 | US$ 512,50 |
| 200 | US$ 57,75 | US$ 294,00 | US$ 2.050,00 |

Leitura: a faixa de US$ 2–6 por partida da auditoria fica entre os cenários base e pessimista. A incerteza dominante é
`r` (P2), um fator de 4× entre otimista e pessimista, multiplicado pela incerteza de preço. **Por isso medir OPS-1 é
critério do gate da Onda 1.**

## 4. Custo de desenvolvimento

- Premissa da auditoria: US$ 100–300 em GPU durante o desenvolvimento (estimativa a validar).
- Controle: registrar cada sessão de GPU (data, provedor, tipo de GPU, horas, US$, objetivo, run_id) — log a criar na
  Onda 1 em `docs/` (por exemplo, `docs/COST_LOG.md`).
- Teto de gasto configurado no provedor (ação humana, ADR-0004).

## 5. Critério de alerta

Se o `custo_partida` medido na Onda 1 projetar acima do preço que o mercado-alvo aceita pagar (desconhecido — validar com
clientes), reabrir o escopo antes da Onda 2: reduzir `r` (stride, modelo menor) ou restringir o produto.
