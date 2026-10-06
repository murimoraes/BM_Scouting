# Avaliação — métricas, ground truth e alvos

> **Regra:** nenhum valor-alvo abaixo foi medido. Todos são **"alvo inicial — a calibrar com dados reais"**.
> Um alvo só muda de status para "validado" com: comando executado, partida(s) usada(s), arquivo de métricas em
> `data/runs/<run_id>/metrics.json` e registro no relatório de auditoria da onda.

## 1. Princípios

1. **Medir no tipo de vídeo-alvo.** Benchmarks públicos medem capacidade genérica; os gates usam ground truth (GT) do tipo
   de vídeo escolhido na ADR-0001.
2. **Holdout trancado.** Uma partida de GT nunca é usada para ajuste; só para o gate. Acesso registrado.
3. **Alvos congelados antes de medir o holdout.** O alvo de um gate é registrado neste arquivo (com data) **antes** da
   medição no holdout. Mudar o alvo depois exige ADR — evita "mover a trave".
4. **Métrica de produto > métrica acadêmica.** O usuário se importa com o jogador-alvo; métricas globais (IDF1, HOTA)
   são diagnósticas.
5. **Teto humano.** Concordância entre os dois anotadores define o melhor resultado razoável para cada métrica.

## 2. Métricas por etapa

Legenda de alvo: todos **a calibrar com dados reais**. "Gate" indica em qual onda a métrica bloqueia avanço.

### 2.1 Detecção (`detections`)

| ID | Métrica | Definição | Alvo inicial | Gate |
|---|---|---|---|---|
| DET-1 | Recall de jogadores | Caixas GT de jogador/goleiro com IoU ≥ 0,5 com alguma predição ÷ caixas GT | ≥ 0,95 | 1 |
| DET-2 | Precisão de jogadores | Predições casadas ÷ predições (classe pessoa) | ≥ 0,90 | 1 |
| DET-3 | Recall de bola | Bola GT com predição a ≤ R px (R definido na Onda 3 conforme resolução) ÷ frames com bola visível | a definir na Onda 3 | 3 |

### 2.2 Tracking e fragmentação (`tracks`)

| ID | Métrica | Definição | Alvo inicial | Gate |
|---|---|---|---|---|
| TRK-1 | Fragmentação do alvo | Nº de tracklets distintos cobrindo o alvo ÷ 10 min de presença do alvo em quadro; reportar **antes e depois** da reconexão | depois ≤ 2 por 10 min | 1 |
| TRK-2 | Cobertura do alvo | Frames em que o alvo está visível (GT) **e** atribuído à identidade-alvo ÷ frames com alvo visível | ≥ 0,80 | 1 |
| TRK-3 | Pureza do alvo | Frames atribuídos à identidade-alvo em que é de fato o alvo ÷ frames atribuídos | ≥ 0,95 | 1 |
| TRK-4 | Trocas de ID no alvo | Eventos em que a identidade-alvo passa a seguir outro jogador, por 90 min | ≤ 2 | 1 |
| TRK-5 | IDF1 / HOTA (diagnóstico) | Padrão MOT, todos os jogadores, nos clipes anotados | sem alvo (diagnóstico) | — |

Pureza tem alvo mais alto que cobertura de propósito: um mapa de calor com lacunas é aceitável; um mapa de calor com
trechos de **outro jogador** é inaceitável.

### 2.3 Identidade (`player_identity`)

| ID | Métrica | Definição | Alvo inicial | Gate |
|---|---|---|---|---|
| IDN-1 | Acurácia de time | Tracklets com `team_label` correto ÷ tracklets avaliados | ≥ 0,95 | 1 |
| IDN-2 | Top-1 do candidato | Partidas em que o candidato rank 1 é o alvo | ≥ 0,70 | 1 |
| IDN-3 | Top-3 (sucesso do 1 clique) | Partidas em que o alvo está entre os 3 primeiros candidatos | ≥ 0,90 | 1 |
| IDN-4 | Interações humanas | Cliques/correções necessários por partida até `confirmed` | ≤ 5 | 1 |
| IDN-5 | Legibilidade do número | Frames amostrados com número legível para humano ÷ frames amostrados (mede o **problema**, não o modelo) | sem alvo (caracterização) | 1 |
| IDN-6 | Acerto de leitura | Leituras do modelo corretas ÷ leituras em frames legíveis | ≥ 0,80 | 1 |

### 2.4 Campo e posicionamento (`field_positions`, `stats`)

| ID | Métrica | Definição | Alvo inicial | Gate |
|---|---|---|---|---|
| FLD-1 | Erro de reprojeção | Distância em metros entre pontos de referência do campo anotados e projetados: mediana e p90 | mediana ≤ 1,0 m; p90 ≤ 2,0 m | 2 |
| FLD-2 | Homografia válida | Frames com homografia `ok` ÷ frames processados | ≥ 0,90 (câmera fixa); a definir (TV) | 2 |
| FLD-3 | Erro de posição do jogador | Distância em metros entre pé do alvo anotado e projetado (mediana, p90) | mediana ≤ 1,0 m | 2 |
| FLD-4 | Erro de distância percorrida | \|d_pred − d_ref\| ÷ d_ref em janelas de 5 min; referência = trajetória GT anotada (ou GPS/EPTS, se disponível com direitos) | ≤ 10 % | 2 |

Atenção (FLD-4): distância é muito sensível a ruído e suavização; ruído de posição soma distância falsa. Medir sempre com
e sem suavização e reportar o parâmetro usado.

### 2.5 Eventos (`events`)

Casamento predição↔GT: mesmo tipo, mesmo ator, |Δt| ≤ τ (τ inicial = 1,0 s, a calibrar).

| ID | Métrica | Alvo inicial (precisão / recall) | Gate |
|---|---|---|---|
| EVT-1 | Passe do alvo | ≥ 0,80 / ≥ 0,70 | 3 |
| EVT-2 | Chute do alvo | ≥ 0,80 / ≥ 0,80 | 3 |
| EVT-3 | Desarme do alvo | ≥ 0,60 / ≥ 0,50 | 3 |
| EVT-4 | Desfecho do passe (certo/errado) | acurácia ≥ 0,80 nos passes casados | 3 |
| EVT-5 | Localização do evento | erro mediano ≤ 2,0 m | 3 |

### 2.6 Estatísticas e relatório (`stats`, `report_input`)

| ID | Métrica | Definição | Alvo | Gate |
|---|---|---|---|---|
| STA-1 | Consistência | `stats` recomputado a partir de `events`/`field_positions` dá resultado idêntico (teste determinístico) | 100 % | 4 |
| STA-2 | Erro de contagem | \|contagem prevista − GT\| por tipo de evento, por partida | derivado de EVT-* | 4 |
| REP-1 | Números não rastreáveis | Números no texto do relatório que não existem em `report_input.facts` | **0 (regra rígida, não calibrável)** | 4 |
| REP-2 | Citação | Afirmações quantitativas com `fact_id` ÷ afirmações quantitativas | 100 % | 4 |
| REP-3 | Avaliação humana | Nota 1–5 de utilidade e fidelidade por avaliador, amostra de relatórios | ≥ 4 (a calibrar) | 4 |

### 2.7 Operação e custo

| ID | Métrica | Definição | Alvo inicial | Gate |
|---|---|---|---|---|
| OPS-1 | Razão de processamento | GPU-min ÷ min de vídeo, por etapa | medir na Onda 1 (premissa do COST_MODEL) | 1 |
| OPS-2 | Custo por partida | ver [COST_MODEL.md](COST_MODEL.md) | ≤ US$ 6 (premissa da auditoria, estimativa a validar) | 1, 5 |
| OPS-3 | Tempo de parede | upload → relatório | a definir na Onda 5 | 5 |
| OPS-4 | Taxa de falha de job | jobs sem relatório ÷ jobs | a definir na Onda 5 | 5 |
| OPS-5 | Tempo de anotação | horas-pessoa por partida de GT, por tipo de anotação | medir no 1º clipe | 1 |

## 3. Protocolo do conjunto de ground truth

### 3.1 Pré-requisitos (bloqueantes)

- ADR-0001 aceita (tipo de vídeo-alvo).
- Para cada partida: **autorização escrita** de quem detém os direitos sobre o vídeo para uso em desenvolvimento e
  avaliação; registro da base legal LGPD. **Não usar partidas com menores de idade** no GT inicial, salvo autorização
  dos responsáveis obtida via clube e registrada (ver RISKS R-11).
- Armazenamento fora de pastas sincronizadas (RISKS R-15).

### 3.2 Seleção

- **3 partidas** do tipo de vídeo-alvo (mínimo 2 se houver restrição de acesso; nesse caso o gate passa a usar
  validação cruzada entre as 2 e isso é registrado como limitação).
- Diversidade desejada: uniformes de cores próximas em ao menos uma partida, iluminação diferente (dia/noite), gramados
  com marcação de qualidades diferentes.
- Divisão: **P1, P2 = desenvolvimento**; **P3 = holdout trancado**.
- Por partida, escolher **1 jogador-alvo** (e, se o esforço permitir, um 2º de outra posição).

### 3.3 O que anotar (amostra, não a partida inteira)

Quantidades são **estimativas a validar**: medir OPS-5 no primeiro clipe e reajustar antes de continuar.

| Camada | Escopo por partida | Uso |
|---|---|---|
| A. Caixas + ID de todos | 10 clipes de 30 s, estratificados (início/fim de cada tempo, bola parada, transição, aglomeração), keyframes a cada 0,5 s com interpolação revisada | DET-1/2, TRK-5, IDN-1 |
| B. Presença do alvo | Partida inteira: intervalos em que o alvo está em quadro | TRK-2 (denominador) |
| C. Pé do alvo | 1 ponto a cada 5 s quando visível (clique no ponto de contato) | TRK-2/3/4, FLD-3, FLD-4 |
| D. Número legível | Nos frames da camada A: para cada jogador, número legível sim/não e valor | IDN-5, IDN-6 |
| E. Pontos do campo | 30 frames espaçados uniformemente: interseções de linhas visíveis com coordenadas conhecidas | FLD-1, FLD-2 |
| F. Eventos do alvo | Partida inteira: passe, chute, desarme, interceptação, com tempo, desfecho e posição aproximada | EVT-* (Onda 3) |
| G. Bola | Nos frames da camada A: centro da bola ou "não visível" | DET-3 (Onda 3) |

Camadas A–E são necessárias para o gate da Onda 1/2; F–G podem ser feitas no início da Onda 3.

### 3.4 Procedimento

1. Escrever o **guia de anotação** (definições operacionais de cada evento, o que conta como "visível", como marcar o pé)
   antes de anotar. Definições de evento entram no guia na Onda 3.
2. Ferramenta: candidata **CVAT** ou **Label Studio** (ambas open source; licença e hospedagem a verificar; instalação
   exige aprovação humana — fora do escopo da Onda 0).
3. Exportar para os **mesmos contratos** (`tracks`, `field_positions`, `events`) com `producer.module = "human_annotation"`,
   mais um `manifest.json` por partida (anotador, data, camadas, versão do guia).
4. **Dupla anotação** de ~10 % (1 clipe de cada camada) pelos dois sócios; registrar concordância (IoU médio, F1 de
   eventos entre anotadores) como teto humano.
5. Congelar a versão do GT (hash do diretório) antes de medir qualquer gate.

## 4. Fontes públicas candidatas

**Nenhuma foi baixada.** Licenças e termos **a verificar** antes de qualquer download (exige aprovação humana). Hipótese
de trabalho: datasets acadêmicos frequentemente proíbem uso comercial ou exigem NDA; modelos treinados com eles podem herdar
restrições. Uso pretendido: comparação de sanidade e desenvolvimento, **não** substituto do GT do tipo de vídeo-alvo.

| Fonte | Conteúdo relevante (conforme descrição pública; confirmar) | Uso pretendido | Licença/termos |
|---|---|---|---|
| SoccerNet (tarefas de tracking, calibração de câmera, game state reconstruction, jersey number, ReID) | Vídeos de transmissão com anotações de MOT, linhas do campo, números de camisa | Sanidade de detecção/tracking/homografia em vídeo de TV; benchmark de leitura de número | **A verificar** — acesso a vídeos condicionado a acordo (NDA); uso comercial provavelmente restrito |
| SportsMOT | MOT em esportes, incluindo futebol | Sanidade de tracking | **A verificar** (possivelmente não comercial) |
| Dados abertos de tracking/eventos sem vídeo (ex.: amostras públicas de provedores de dados esportivos) | Trajetórias em metros e eventos anotados | Desenvolver `events`/`stats` **sem** depender da visão (contrato `field_positions` como entrada) | **A verificar** caso a caso |

## 5. Como uma métrica vira evidência

```
1. Comando executado (registrado no relatório): ex. python -m bm_scouting.eval ... (a criar na Onda 1)
2. Saída: data/runs/<run_id>/metrics.json com: métrica, valor, partida(s), versão do GT, hashes dos artefatos, commit
3. Relatório de auditoria cita run_id e compara com o alvo congelado → PASSOU/FALHOU
```
Afirmação sem `run_id` é reprovada pelo QA/Auditor.
