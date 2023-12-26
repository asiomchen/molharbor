import pytest
from pymolport.checker import Molport, SearchType, UnknownSearchTypeException

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
@pytest.mark.parametrize("search_type", [
    "exact",
    "similarity",
    "substructure",
    "superstructure",
    10,
    100,
])
def test_find_invalid_search_type(search_type):
    molport = Molport()
    smiles = "C1=CC=CC=C1"
    max_results = 1000
    similarity = 0.9

    with pytest.raises(UnknownSearchTypeException):
        molport.find(smiles, search_type, max_results, similarity)
@pytest.mark.parametrize("smiles", [
    "VCX",
    "cCcccc123",
])
def test_find_invalid_smiles(smiles):
    molport = Molport()
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9
    result = molport.find(smiles, search_type, max_results, similarity) 
    assert result == [None]