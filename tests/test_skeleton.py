"""Garante que o esqueleto de pacotes existe, importa e documenta sua responsabilidade."""

import importlib

import pytest

MODULES = ["detection", "tracking", "identity", "field", "events", "stats", "report", "pipeline"]


@pytest.mark.parametrize("name", MODULES)
def test_module_imports_and_has_docstring(name):
    module = importlib.import_module(f"bm_scouting.{name}")
    assert module.__doc__ and "Responsabilidade" in module.__doc__
