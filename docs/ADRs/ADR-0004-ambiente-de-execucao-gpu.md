# ADR-0004 — Localização de GPU e ambiente de execução

- Status: **Proposta — aguarda decisão humana**
- Data da proposta: 2026-10-05
- Decisor(es): — | Data da decisão: —

## Contexto

Sem GPU local garantida; orçamento de desenvolvimento estimado em US$ 100–300 (premissa da auditoria, a validar).
Os vídeos contêm imagem de pessoas (dado pessoal) e possivelmente menores. O repositório atual está numa pasta sincronizada
do OneDrive de uma organização (ver RISKS R-15). Preços de GPU **não** são citados aqui: consultar valores vigentes no
momento da decisão e registrar em COST_MODEL.md.

## Opções

**A. Marketplace de GPUs de terceiros** (ex.: Vast.ai) — máquinas de hosts variados, geralmente mais baratas; segurança
física/lógica depende do host.

**B. Provedor de GPU com datacenter próprio/parceiro verificado** (ex.: modalidades "secure cloud"/serverless de provedores
como RunPod) — preço intermediário, cobrança por hora ou por segundo, imagens de contêiner.

**C. Nuvem grande** (AWS/GCP/Azure), possivelmente em região São Paulo — mais caro, mais controles, residência de dados no
Brasil possível.

**D. Notebooks gratuitos/baratos** (Colab/Kaggle) — bons para experimentos curtos; termos de uso limitam uso comercial e
automação (verificar); sessões instáveis.

**E. CPU local** para tudo que não é rede neural (tracking, homografia estática, eventos, stats, testes).

## Trade-offs

| Critério | A | B | C | D | E |
|---|---|---|---|---|---|
| Custo/hora | Mais baixo (verificar) | Médio | Mais alto | ~0 | 0 |
| Confiança no host p/ vídeo com dado pessoal | **Baixa** | Média–alta | Alta | Média | Alta |
| Transferência internacional (LGPD art. 33) | Sim, país do host variável | Sim (verificar regiões) | Evitável (região BR) | Sim | Não |
| Reprodutibilidade (contêiner) | Sim | Sim | Sim | Parcial | Sim |
| Caminho para produção | Fraco | Bom (serverless + fila) | Bom | Nenhum | — |

## Recomendação

- **Desenvolvimento:** E para tudo que roda em CPU; **B** para lotes curtos de GPU, sempre a partir da mesma imagem de
  contêiner, desligando a máquina ao fim de cada lote (registrar horas em log de custo). Em B, usar **somente** vídeos com
  autorização e, enquanto não houver análise jurídica, **nenhum vídeo com menores**.
- **A (marketplace) só com dados públicos/licenciados** sem dado pessoal sensível — nunca com vídeos de clientes ou de base.
- **Produção (Onda 5):** decidir entre B serverless e C com base em custo medido (OPS-1/OPS-2) e parecer LGPD sobre
  transferência internacional. Registrar em nova ADR.
- **Não armazenar vídeos ou artefatos no OneDrive** do diretório atual.

## Consequências

- Onda 1 precisa de um Dockerfile e de um procedimento "subir máquina → rodar etapa → baixar artefatos → destruir máquina"
  (o Dockerfile está fora do escopo de arquivos da Onda 0; requer aprovação).
- Controle de gasto: teto mensal configurado no provedor (ação humana).

## O que nos faria mudar de ideia

- Aparecer GPU local/doada adequada.
- Parecer jurídico considerar aceitável o uso de marketplace com criptografia e retenção zero.

## Decisão humana

_(preencher: provedor(es) para desenvolvimento, teto de gasto mensal, política de dados em GPU alugada, decisor, data)_
