import pytest
from pymolport.data import Molecule, Data, Result, Response

example_mol = {
        "Id": 2266780,
        "MolPort Id": "Molport-002-266-780",
        "SMILES": "Cc1ccc(cc1)C(=O)OCc1ccc(cc1)C#N",
        "Canonical SMILES": "Cc1ccc(cc1)C(=O)OCc1ccc(cc1)C#N",
        "Verified Amount": 100,
        "Unverified Amount": 100,
        "Similarity Index": 0.80487806
      }


def test_molecule():
    mol = Molecule(example_mol)
    assert mol.id == 2266780
    assert mol.molport_id == "Molport-002-266-780"
    assert mol.smiles == "Cc1ccc(cc1)C(=O)OCc1ccc(cc1)C#N"
    assert mol.canonical_smiles == "Cc1ccc(cc1)C(=O)OCc1ccc(cc1)C#N"
    assert mol.verified_amount == 100.0
    assert mol.unverified_amount == 100.0
    assert mol.similarity_index == 0.80487806