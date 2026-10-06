"""Módulo Relatório/LLM.

Responsabilidade: montar report_input (fatos numerados) e gerar o texto do
relatório via LLM restrito a esses fatos; verificar que todo número do texto
é rastreável a um fact_id.
Consome: stats v1 + events v1 + player_identity v1. Produz: report_input v1.
Dono: agente Relatório/LLM. Sem implementação na Onda 0."""
