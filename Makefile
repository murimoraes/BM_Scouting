# Comandos do projeto. No Windows sem `make`, rode os comandos equivalentes diretamente
# (ver CLAUDE.md, seção "Comandos").
PYTHON ?= python

.PHONY: test contracts install-dev

## Roda toda a suíte de testes.
test:
	$(PYTHON) -m pytest

## Valida JSON Schemas (meta-schema), exemplos válidos e mutações inválidas.
contracts:
	$(PYTHON) -m pytest tests/test_contracts.py -v

## Instala dependências de desenvolvimento (acessa a rede: pytest e jsonschema apenas).
install-dev:
	$(PYTHON) -m pip install -e ".[dev]"
