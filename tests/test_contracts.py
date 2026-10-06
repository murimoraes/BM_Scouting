"""Valida os contratos JSON (docs/contracts/v1).

Três garantias:
1. Todo schema é um JSON Schema 2020-12 válido (meta-schema).
2. Todo contrato tem exemplo e o exemplo valida contra o schema.
3. Mutações inválidas conhecidas são REJEITADAS (prova de que o schema restringe algo;
   um schema permissivo demais faria o item 2 passar trivialmente).
"""

import copy
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator
from referencing import Registry, Resource

CONTRACTS_DIR = Path(__file__).resolve().parent.parent / "docs" / "contracts" / "v1"
EXAMPLES_DIR = CONTRACTS_DIR / "examples"

ARTIFACTS = [
    "detections",
    "tracks",
    "player_identity",
    "field_positions",
    "events",
    "stats",
    "report_input",
]


def _load(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


SCHEMAS = {p.name.removesuffix(".schema.json"): _load(p) for p in CONTRACTS_DIR.glob("*.schema.json")}
REGISTRY = Registry().with_resources(
    (schema["$id"], Resource.from_contents(schema)) for schema in SCHEMAS.values()
)


def _validator(name: str) -> Draft202012Validator:
    return Draft202012Validator(SCHEMAS[name], registry=REGISTRY)


def _example(name: str):
    return _load(EXAMPLES_DIR / f"{name}.example.json")


def _set_pointer(doc, pointer: str, value):
    """Define `value` no caminho JSON Pointer simples `pointer` (sem escapes ~0/~1)."""
    parts = pointer.strip("/").split("/")
    node = doc
    for part in parts[:-1]:
        node = node[int(part)] if isinstance(node, list) else node[part]
    last = parts[-1]
    if isinstance(node, list):
        node[int(last)] = value
    else:
        node[last] = value


def test_every_artifact_has_schema():
    assert set(ARTIFACTS) | {"common"} == set(SCHEMAS), sorted(SCHEMAS)


@pytest.mark.parametrize("name", sorted(SCHEMAS))
def test_schema_is_valid_2020_12(name):
    Draft202012Validator.check_schema(SCHEMAS[name])


@pytest.mark.parametrize("name", ARTIFACTS)
def test_schema_id_matches_filename(name):
    assert SCHEMAS[name]["$id"].endswith(f"/contracts/v1/{name}.schema.json")


@pytest.mark.parametrize("name", ARTIFACTS)
def test_example_is_valid(name):
    errors = sorted(_validator(name).iter_errors(_example(name)), key=str)
    assert not errors, "\n".join(f"{list(e.absolute_path)}: {e.message}" for e in errors)


@pytest.mark.parametrize("name", ARTIFACTS)
def test_example_header_names_its_schema(name):
    assert _example(name)["header"]["schema_name"] == name


@pytest.mark.parametrize("name", ARTIFACTS)
def test_unknown_root_field_is_rejected(name):
    doc = _example(name)
    doc["unexpected_field"] = 1
    assert not _validator(name).is_valid(doc)


INVALID_MUTATIONS = [
    ("detections", "/frames/0/detections/0/confidence", 1.5),
    ("detections", "/frames/0/detections/0/bbox_xyxy", [1.0, 2.0, 3.0]),
    ("detections", "/header/schema_name", "tracks"),
    ("tracks", "/tracklets/0/observations", []),
    ("tracks", "/header/video/sha256", "abc"),
    ("tracks", "/header/schema_version", "2.0.0"),
    ("player_identity", "/selection/status", "confirmed"),  # confirmado sem confirmed_by
    ("player_identity", "/query/jersey_number", 100),
    ("field_positions", "/homography/estimates/0/H", [[1, 0, 0], [0, 1, 0]]),
    ("field_positions", "/field/length_m", 130),
    ("events", "/events/0/type", "goal_celebration"),
    ("events", "/events/0/event_id", "1"),
    ("stats", "/metrics/sprints/reliability", "high"),  # valor null exige 'unavailable'
    ("stats", "/coverage/tracked_fraction", 1.2),
    ("report_input", "/generation_constraints/only_listed_facts", False),
    ("report_input", "/facts/0/fact_id", "fato-1"),
]


@pytest.mark.parametrize("name,pointer,value", INVALID_MUTATIONS)
def test_invalid_mutation_is_rejected(name, pointer, value):
    doc = copy.deepcopy(_example(name))
    _set_pointer(doc, pointer, value)
    assert not _validator(name).is_valid(doc), f"{name}{pointer}={value!r} deveria ser inválido"
