import pytest
from pymolport.checker import Molport, SearchType, UnknownSearchTypeException
from typing import Iterable

def test_find_single_smiles():
    molport = Molport()
    smiles = "C1=CC=CC=C1"
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9

    result = molport.find(smiles, search_type, max_results, similarity)

    assert isinstance(result, list)
    assert len(result) == 1

def test_find_multiple_smiles():
    molport = Molport()
    smiles = ["C1=CC=CC=C1", "C1=CC=CC=C2C(=C1)C=CC=C2"]
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9

    result = molport.find(smiles, search_type, max_results, similarity)

    assert isinstance(result, list)
    assert len(result) == len(smiles)

def test_find_invalid_search_type():
    molport = Molport()
    smiles = "C1=CC=CC=C1"
    search_type = "INVALID"
    max_results = 1000
    similarity = 0.9

    with pytest.raises(UnknownSearchTypeException):
        molport.find(smiles, search_type, max_results, similarity)

def test_find_invalid_smiles_type():
    molport = Molport()
    smiles = 12345  # Not a string or iterable of strings
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9

    with pytest.raises(TypeError):
        molport.find(smiles, search_type, max_results, similarity)