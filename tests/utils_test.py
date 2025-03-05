from molharbor import utils
from molharbor.enums import SearchType
import pytest


@pytest.mark.parametrize(
    "smiles, search_type, max_results, similarity, credentials",
    [
        (
            "CCO",
            SearchType.EXACT,
            10,
            0.8,
            {"username": "john.spade", "password": "password"},
        ),
        ("CCO", SearchType.SIMILARITY, 10, 0.8, {"api_key": "key"}),
        ("CCO", SearchType.SIMILARITY, 10, 0.8, {"api_key": "key"}),
        (
            "CCO",
            SearchType.SIMILARITY,
            100,
            0.8,
            {"username": "john.spade", "password": "password"},
        ),
        (
            "CCO",
            SearchType.SIMILARITY,
            100,
            0.68,
            {"username": "john.spade", "password": "password"},
        ),
        ("CCO", SearchType.SIMILARITY, 100, 0.08, {"api_key": "key"}),
    ],
)
def test_compound_search_payload_api(
    smiles, search_type, max_results, similarity, credentials
):
    expected_payload = {
        "Structure": smiles,
        "Search Type": SearchType(search_type).value,
        "Maximum Result Count": max_results,
        "Chemical Similarity Index": similarity,
        **credentials,
    }
    expected_payload = {k: v for k, v in expected_payload.items() if v is not None}
    if "username" in expected_payload:
        expected_payload["User Name"] = expected_payload.pop("username")
    if "password" in expected_payload:
        expected_payload["Authentication Code"] = expected_payload.pop("password")
    if "api_key" in expected_payload:
        expected_payload["API Key"] = expected_payload.pop("api_key")
    result = utils.compound_search_payload(
        smiles=smiles,
        search_type=search_type,
        max_results=max_results,
        similarity=similarity,
        credentials=credentials,
    )
    for key, value in expected_payload.items():
        assert key in result, f"Key {key} not found in result"
        assert result[key] == value, f"Value {value} not found in result"


def test_api_key_is_default():
    smiles = "CCO"
    search_type = SearchType.SIMILARITY
    max_results = 100
    similarity = 0.8
    credentials = {"username": "john.spade", "password": "password", "api_key": "key"}
    result = utils.compound_search_payload(
        smiles=smiles,
        search_type=search_type,
        max_results=max_results,
        similarity=similarity,
        credentials=credentials,
    )
    assert "API Key" in result, "Key API Key not found in result"
    assert result.get("API Key") == "key", (
        f"API Key is not equal to key, {result.get('API Key')}"
    )
    assert not result.get("User Name", False), (
        f"User Name is not empty, {result.get('User Name')}"
    )
    assert not result.get("Authentication Code", False), (
        f"Authentication Code is not empty, {result}"
    )
