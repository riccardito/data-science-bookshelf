import hashlib
import importlib.util
import json
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "check_private_terms", Path(__file__).parents[1] / "scripts" / "check_private_terms.py")
cpt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cpt)

PLANTED = frozenset({hashlib.sha256(b"zebrafinch").hexdigest()})


def test_a_planted_word_is_found_case_blind():
    assert cpt.hits(["nothing here", "a ZebraFinch sings", "zebrafinches"], PLANTED) == [2]


def test_the_shipped_list_is_seven_hashes():
    assert len(cpt.PRIVATE_SHA256) == 7
    assert all(len(h) == 64 for h in cpt.PRIVATE_SHA256)


def test_notebook_outputs_are_read_too(tmp_path):
    nb = {"cells": [{"source": ["x = 1\n"], "outputs": [{"text": ["the zebrafinch\n"]},
                                                       {"data": {"text/plain": "zebrafinch"}}]}]}
    p = tmp_path / "c.ipynb"
    p.write_text(json.dumps(nb), encoding="utf-8")
    assert cpt.hits(cpt.notebook_lines(p), PLANTED) == [2, 3]
