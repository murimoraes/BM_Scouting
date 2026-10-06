# Registro de riscos

Escala: Probabilidade (P) e Impacto (I) em **A**lto / **M**édio / **B**aixo — avaliação qualitativa, a revisar a cada
gate. Donos: **Murilo**, **Sócio** (nome a preencher) e o papel de agente responsável (ver [AGENTS.md](AGENTS.md)).
Riscos jurídicos abaixo **não são parecer jurídico**: recomenda-se consulta a advogado(a) com experiência em LGPD e
direito desportivo/autoral antes da Onda 5 e, para R-09/R-11, antes de coletar o GT.

| ID | Risco | P | I | Mitigação | Dono | Gatilho de revisão |
|---|---|---|---|---|---|---|
| R-01 | Tipo de vídeo indefinido torna o MVP inviável ou mal direcionado | A | A | ADR-0001 decidida antes da Onda 1; especificação mínima de vídeo e recusa na ingestão | Murilo + Sócio | Gate 0 |
| R-02 | Homografia dinâmica (pan/zoom) é problema de pesquisa | A (TV) / B (fixa) | A | Câmera fixa (ADR-0001); spike de homografia na Onda 1 com resultado medido (FLD-1/2) | Agente Campo | Fim do spike 1.S |
| R-03 | Número da camisa raramente legível | A | A | Votação por tracklet + 1 clique + fallback manual (ADR-0002); medir IDN-5 para conhecer o problema | Agente Identidade | Gate 1 |
| R-04 | Fragmentação de IDs em 90 min contamina trajetória do alvo | A | A | Reconexão espaço-temporal, pureza > cobertura, métricas TRK-1..4 (ADR-0003) | Agente Tracking | Gate 1 |
| R-05 | Bola pequena/borrada; sem modelo próprio, eventos falham | A | M | Modelo de bola dedicado na Onda 3; eventos por regras; declarar baixa confiabilidade | Agente Vision | Gate 3 |
| R-06 | Sem ground truth, progresso não é mensurável | A | A | Protocolo de GT (EVALUATION §3) como fase 1.0 da Onda 1; gate exige métricas no holdout | Agente QA | Gate 1 |
| R-07 | Custo de GPU por partida acima do sustentável | M | A | Modelo de custo com cenários; OPS-1 medido na Onda 1; alavancas (stride, modelo menor) | Agente Backend/Infra | Gate 1, Gate 5 |
| R-08 | Licença AGPL do detector inviabiliza SaaS fechado | M | A | ADR-0006: detector com licença permissiva verificada; inventário de licenças | Murilo | Antes da fase 1.2 |
| R-09 | **Direitos sobre o vídeo:** usuário envia vídeo cujo direito não detém (ex.: transmissão de TV); uso em GT sem autorização | A (TV) / M | A | Termos de uso com declaração de titularidade/autorização; GT só com autorização escrita; preferir câmera própria do clube (ADR-0001) | Sócio | Antes do GT; Onda 5 |
| R-10 | **LGPD — dados pessoais e possivelmente biométricos:** imagem de jogadores é dado pessoal; embeddings de aparência para reidentificar pessoas podem ser enquadrados como dado biométrico (dado sensível, art. 5º II e art. 11) | A | A | Minimização (`match_id` opaco, sem nome por padrão); embeddings efêmeros (ADR-0003); retenção curta de vídeos e recortes; base legal registrada; RIPD/DPIA antes da Onda 5 | Sócio | Antes do GT; Onda 5 |
| R-11 | **Menores de idade em categorias de base:** tratamento de dados de crianças e adolescentes exige melhor interesse e, para crianças, consentimento específico de responsável (LGPD art. 14) | A (se ADR-0001 = B) | A | Não usar vídeos com menores no GT inicial sem autorização dos responsáveis via clube; fluxo de consentimento no produto antes de aceitar clientes de base; parecer jurídico | Sócio | Decisão da ADR-0001 |
| R-12 | Datasets/pesos públicos com licença não comercial ou NDA contaminam o produto | M | A | Nenhum download sem verificar licença (aprovação humana); inventário de licença de dados/pesos; GT próprio como base dos gates | Agente QA | Qualquer download |
| R-13 | LLM inventa números/fatos no relatório | M | A | `report_input` como única fonte; citação obrigatória de `fact_id`; verificação automática REP-1 = 0 | Agente Relatório | Gate 4 |
| R-14 | Capacidade de 2 pessoas / escopo cresce | A | M | Ondas com gates binários; CLAUDE.md proíbe antecipar ondas; máximo 3 subagentes | Murilo | Todo gate |
| R-15 | **Repositório em pasta OneDrive de organização** (Fundação Salvador Arena): vídeos e dados pessoais seriam sincronizados para nuvem de terceiro; possível conflito de política interna/propriedade intelectual do empregador sobre trabalho feito nessa conta | M | A | Mover o projeto para pasta não sincronizada e repositório git próprio; `data/` nunca dentro de pasta sincronizada; verificar política da organização | Murilo | **Imediato** |
| R-16 | Projeto sem controle de versão (não é repositório git) | A | M | `git init` + remoto privado (requer aprovação; fora do escopo de arquivos da Onda 0); `.gitignore` excluindo `data/` | Murilo | Imediato |
| R-17 | Vídeo com dado pessoal processado em host não confiável (marketplace de GPU) ou com transferência internacional sem base | M | A | ADR-0004: marketplace só com dados públicos; avaliar residência de dados para produção | Agente Backend/Infra | Antes da 1ª execução em GPU |
| R-18 | Usuários confiam em estatística imprecisa (dano reputacional, decisão de contratação errada) | M | A | `reliability` e `coverage` obrigatórios; relatório declara limitações; não exibir métrica `unavailable` | Agente Relatório | Gate 4 |
| R-19 | Variabilidade de vídeo (iluminação, compressão, fps variável, gramado sintético sem marcação) | A | M | Especificação mínima de entrada; GT diverso; checagens na ingestão | Agente Vision | Gate 1 |
| R-20 | Artefatos por frame muito grandes (disco/memória) | M | M | ADR-0005 (gzip, medir; Parquet se necessário) | Agente Backend/Infra | Fase 1.1 |
| R-21 | Alvos de métrica ajustados após ver o resultado ("mover a trave") | M | M | Alvos congelados antes do holdout; mudança só por ADR (EVALUATION §1) | Agente QA | Todo gate |
