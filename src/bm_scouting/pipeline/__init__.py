"""Orquestração e cache de artefatos.

Responsabilidade: executar as etapas em ordem, calcular a chave de cache de
cada artefato (hash de entradas + versão do módulo + config), pular etapas
com cache válido e validar todo artefato contra seu JSON Schema.
Dono: agente Backend/Infra. Sem implementação na Onda 0."""
