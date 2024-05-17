import pytest
from pytest import MonkeyPatch
from molharbor import Molport, SearchType, UnknownSearchTypeException
from molharbor.exceptions import LoginError
from .mock import MockResponse


@pytest.fixture
def molport():
    molport = Molport()
    molport.login(username="john.spade", password="fasdga34a3")
    return molport


@pytest.mark.parametrize(
    "username, password",
    [
        ("admin", "admin"),
        ("unknown user", "fasdga34a3"),
        (";lkjhgfdg", "tyguhiujokplp;"),
    ],
)
def test_invalid_username_password(username, password):
    molport = Molport()
    molport.login(username=username, password=password)
    with pytest.raises(LoginError):
        molport.find("C1=CC=CC=C1", SearchType.EXACT, 1000, 0.9)


@pytest.mark.parametrize(
    "api_key",
    [
        "da39654c-145d-11ef-a3b0-00155d8905e7",
        "e0f2970a-145d-11ef-a3b0-00155d8905e7",
        "e7a0c856-145d-11ef-a3b0-00155d8905e7",
    ],
)
def test_invalid_api_key(api_key):
    molport = Molport()
    molport.login(api_key=api_key)
    with pytest.raises(LoginError):
        molport.find("C1=CC=CC=C1", SearchType.EXACT, 1000, 0.9)


def test_user_and_api_key(molport):
    with pytest.raises(LoginError):
        molport.login(
            username="john.spade",
            password="fasdga34a3",
            api_key="da39654c-145d-11ef-a3b0-00155d8905e7",
        )


def test_no_login(molport):
    molport = Molport()
    with pytest.raises(LoginError):
        molport.find("C1=CC=CC=C1", SearchType.EXACT, 1000, 0.9)


def test_user_no_password(molport):
    molport = Molport()
    with pytest.raises(LoginError):
        molport.login(username="john.spade")


def test_find_single_smiles(molport):
    smiles = "C1=CC=CC=C1"
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9

    result = molport.find(smiles, search_type, max_results, similarity)

    assert isinstance(result, list)
    assert len(result) == 1


def test_find_multiple_smiles(molport):
    smiles = ["C1=CC=CC=C1", "C1=CC=CC=C2C(=C1)C=CC=C2"]
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9

    result = molport.find(smiles, search_type, max_results, similarity)

    assert isinstance(result, list)
    assert len(result) == len(smiles)


@pytest.mark.parametrize(
    "search_type",
    [
        "exact",
        "similarity",
        "substructure",
        "superstructure",
        10,
        100,
    ],
)
def test_find_invalid_search_type(molport, search_type):
    smiles = "C1=CC=CC=C1"
    max_results = 1000
    similarity = 0.9

    with pytest.raises(UnknownSearchTypeException):
        molport.find(smiles, search_type, max_results, similarity)


@pytest.mark.parametrize(
    "smiles",
    [
        "VCX",
        "cCcccc123",
    ],
)
def test_find_invalid_smiles(molport, smiles):
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9
    result = molport.find(smiles, search_type, max_results, similarity)
    assert result == [[None]]


def test_invalid_response(molport, monkeypatch: MonkeyPatch):
    def mock_response(*args, **kwargs):
        return {"error": "Invalid response"}

    monkeypatch.setattr("httpx.Response.json", mock_response)
    smiles = "C1=CC=CC=C1"
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9
    result = molport.find(smiles, search_type, max_results, similarity)
    assert result == [[None]]


def test_unsuccessful_response(molport: Molport, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "httpx.Client.post",
        lambda *args, **kwargs: MockResponse(400, {"error": "Invalid response"}),
    )
    smiles = "C1=CC=CC=C1"
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9
    result = molport.find(smiles, search_type, max_results, similarity)
    assert result == [[None]]
