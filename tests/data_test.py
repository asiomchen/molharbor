import json
import pytest
from pathlib import Path
from pydantic import ValidationError
from molharbor.data import Molecule, Response, SearchPayload

example_mol = {
    "Id": 2266780,
    "MolPort Id": "Molport-002-266-780",
    "SMILES": "Cc1ccc(cc1)C(=O)OCc1ccc(cc1)C#N",
    "Canonical SMILES": "Cc1ccc(cc1)C(=O)OCc1ccc(cc1)C#N",
    "Verified Amount": 100,
    "Unverified Amount": 100,
    "Similarity Index": 0.80487806,
}

EXAMPLE_PATH = Path("tests/data/")
SUCCESSFUL_SEARCH_PATH = EXAMPLE_PATH / "molport_search.json"


def test_molecule():
    mol = Molecule(**example_mol)
    assert mol.id == 2266780
    assert mol.molport_id == "Molport-002-266-780"
    assert mol.smiles == "Cc1ccc(cc1)C(=O)OCc1ccc(cc1)C#N"
    assert mol.canonical_smiles == "Cc1ccc(cc1)C(=O)OCc1ccc(cc1)C#N"
    assert mol.verified_amount == 100.0
    assert mol.unverified_amount == 100.0
    assert mol.similarity_index == 0.80487806


def test_search_response():
    with open(SUCCESSFUL_SEARCH_PATH) as f:
        resp = Response(**json.load(f))
    assert resp.result.status == 1
    assert resp.result.message == "Similarity search completed!"
    assert resp.data.version == "v.1.0"
    assert len(resp.data.molecules) == 1
    assert isinstance(resp.data.molecules[0], Molecule)
    assert resp.data.molecules[0].id == 1740297
    assert resp.data.molecules[0].molport_id == "Molport-001-740-297"
    assert resp.data.molecules[0].smiles == "O=C(OCc1ccccc1)c1ccccc1"
    assert resp.data.molecules[0].canonical_smiles == "O=C(OCc1ccccc1)c1ccccc1"
    assert resp.data.molecules[0].verified_amount == 22475000.0
    assert resp.data.molecules[0].unverified_amount == 25000000.0
    assert resp.data.molecules[0].similarity_index == 1.0


@pytest.mark.parametrize(
    "credentials",
    [
        {"username": "john.spade", "password": "password", "api_key": "key"},
        {"username": "john.spade"},
        {"password": "password"},
        {},
    ],
)
def test_search_payload_invalid_credentials(credentials):
    with pytest.raises(ValidationError):
        SearchPayload(
            smiles="CCO",
            search_type="exact",
            max_results=10,
            similarity=0.8,
            credentials=credentials,
        )
