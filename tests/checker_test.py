import pandas as pd
from pydantic import ValidationError
import pytest
from pytest import MonkeyPatch
from pytest_lazyfixture import lazy_fixture
from molharbor import Molport
from molharbor.enums import SearchType, ResultStatus
from molharbor.exceptions import UnknownSearchTypeException
from molharbor.data import ResponseSupplier, Response
from molharbor.exceptions import LoginError
from .mock import MockResponse, MockResponseSupplier
import json

SEARCH_10_EXACT_SUCCESS = "tests/data/search_10_results_exact.json"
SUP_SEARCH_SUCCESS = "tests/data/suppliers_search.json"
BAD_SMILES_RESPONSE = "tests/data/bad_smiles_search.json"


@pytest.fixture
def molport():
    molport = Molport()
    molport.login(username="john.spade", password="fasdga34a3")
    return molport


@pytest.fixture
def molport_api_key():
    molport = Molport()
    molport.login(api_key="880d8343-8ui2-418c-9g7a-68b4e2e78c8b")
    return molport


@pytest.fixture
def supplier_response():
    with open(SUP_SEARCH_SUCCESS, "r") as f:
        data = json.load(f)
    return ResponseSupplier(**data)


@pytest.fixture
def search_response():
    with open(SEARCH_10_EXACT_SUCCESS, "r") as f:
        data = json.load(f)
    return Response(**data)


@pytest.fixture
def bad_smiles_response():
    with open(BAD_SMILES_RESPONSE, "r") as f:
        data = json.load(f)
    return Response(**data)


def test_molport_repr():
    molport = Molport()
    assert repr(molport) == "Molport()"


def test_api_setter(molport):
    molport.api_key = "880d8343-8ui2-418c-9g7a-68b4e2e78c8b"
    assert molport.api_key == "880d8343-8ui2-418c-9g7a-68b4e2e78c8b"
    assert molport._api_key == "880d8343-8ui2-418c-9g7a-68b4e2e78c8b"
    assert molport.username is None
    assert molport.password is None


def test_username_setter(molport):
    molport.username = "john.spade"
    assert molport.username == "john.spade"
    assert molport._username == "john.spade"


def test_password_setter(molport):
    molport.password = "fasdga34a3"
    assert molport.password == "fasdga34a3"
    assert molport._password == "fasdga34a3"
    assert molport.api_key is None


@pytest.mark.parametrize(
    "username, password",
    [
        ("admin", "admin"),
        ("unknown user", "fasdga34a3"),
        (";lkjhgfdg", "tyguhiujokplp;"),
    ],
)
def test_invalid_username_password(username, password, monkeypatch: MonkeyPatch):
    def mock_response(*args, **kwargs):
        data = {
            "Result": {
                "Status": 2,
                "Message": "User is not recognized or allowed request count exceeded!",
            },
            "Data": {"Version": "v.3.0.2"},
        }
        return MockResponse(200, data)

    monkeypatch.setattr("cloudscraper.CloudScraper.post", mock_response)
    molport = Molport()
    molport.login(username=username, password=password)
    with pytest.raises(LoginError):
        molport.find(
            "C1=CC=CC=C1",
            search_type=SearchType.EXACT,
            max_results=1000,
            similarity=0.9,
        )


@pytest.mark.parametrize(
    "api_key",
    [
        "da39654c-145d-11ef-a3b0-00155d8905e7",
        "e0f2970a-145d-11ef-a3b0-00155d8905e7",
        "e7a0c856-145d-11ef-a3b0-00155d8905e7",
    ],
)
def test_invalid_api_key(api_key, monkeypatch: MonkeyPatch):
    def mock_response(*args, **kwargs):
        data = {
            "Result": {
                "Status": 2,
                "Message": "User is not recognized or allowed request count exceeded!",
            },
            "Data": {"Version": "v.3.0.2"},
        }
        return MockResponse(200, data)

    monkeypatch.setattr("cloudscraper.CloudScraper.post", mock_response)
    molport = Molport()
    molport.login(api_key=api_key)
    with pytest.raises(LoginError):
        molport.find(
            "C1=CC=CC=C1",
            search_type=SearchType.EXACT,
            max_results=1000,
            similarity=0.9,
        )


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
        molport.find(
            "C1=CC=CC=C1",
            search_type=SearchType.EXACT,
            max_results=1000,
            similarity=0.9,
        )


def test_user_no_password(molport):
    molport = Molport()
    with pytest.raises(LoginError):
        molport.login(username="john.spade")


def test_find_single_smiles(
    molport: Molport, search_response: Response, monkeypatch: MonkeyPatch
):
    smiles = "C1=CC=CC=C1"
    search_type = SearchType.EXACT
    max_results = 10
    similarity = 0.9
    monkeypatch.setattr(
        "cloudscraper.CloudScraper.post",
        lambda *args, **kwargs: MockResponse(
            200, search_response.model_dump(by_alias=True)
        ),
    )

    result = molport.find(
        smiles, search_type=search_type, max_results=max_results, similarity=similarity
    )

    assert isinstance(result, list)
    assert len(result) == 8


def test_find_single_smiles_response(
    molport: Molport, search_response: Response, monkeypatch: MonkeyPatch
):
    smiles = "C1=CC=CC=C1"
    search_type = SearchType.EXACT
    max_results = 10
    similarity = 0.9
    monkeypatch.setattr(
        "cloudscraper.CloudScraper.post",
        lambda *args, **kwargs: MockResponse(
            200, search_response.model_dump(by_alias=True)
        ),
    )

    result = molport.find(
        smiles,
        search_type=search_type,
        max_results=max_results,
        similarity=similarity,
        return_response=True,
    )

    assert isinstance(result, Response), "Response is not an instance of Response"
    assert result.result.status == ResultStatus.SUCCESS.value
    assert result.result.message == "Exact search completed!"


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
        molport.find(
            smiles=smiles,
            max_results=max_results,
            similarity=similarity,
            search_type=search_type,
        )


@pytest.mark.parametrize(
    "smiles",
    [
        "VCX",
        "cCcccc123",
    ],
)
def test_find_invalid_smiles(
    molport, smiles, bad_smiles_response: Response, monkeypatch: MonkeyPatch
):
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9
    monkeypatch.setattr(
        "cloudscraper.CloudScraper.post",
        lambda *args, **kwargs: MockResponse(
            200, bad_smiles_response.model_dump(by_alias=True)
        ),
    )
    result = molport.find(
        smiles, search_type=search_type, max_results=max_results, similarity=similarity
    )
    assert result == []


@pytest.mark.parametrize(
    "smiles",
    [
        1000,
        ["C1=CC=CC=C1"],
    ],
)
def test_find_smiles_not_string(molport, smiles):
    with pytest.raises(TypeError):
        molport.find(
            smiles=smiles,
            search_type=SearchType.EXACT,
            max_results=1000,
            similarity=0.9,
        )


def test_invalid_response(molport, monkeypatch: MonkeyPatch):
    def mock_response(*args, **kwargs):
        data = {"error": "Invalid response"}
        return MockResponse(400, data)

    monkeypatch.setattr("cloudscraper.CloudScraper.post", mock_response)
    smiles = "C1=CC=CC=C1"
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9
    with pytest.raises(ValueError):
        molport.find(
            smiles,
            search_type=search_type,
            max_results=max_results,
            similarity=similarity,
        )


def test_unsuccessful_response(molport: Molport, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "cloudscraper.CloudScraper.post",
        lambda *args, **kwargs: MockResponse(400, {"error": "Invalid response"}),
    )
    smiles = "C1=CC=CC=C1"
    search_type = SearchType.EXACT
    max_results = 1000
    similarity = 0.9
    with pytest.raises(ValueError):
        molport.find(
            smiles,
            search_type=search_type,
            max_results=max_results,
            similarity=similarity,
        )


@pytest.mark.parametrize(
    "code, msg",
    [
        (400, "Invalid response"),
        (401, "Unauthorized"),
        (403, "Forbidden"),
        (404, "Not found"),
    ],
)
def test_get_suppliers_unsuccessful_response(
    molport: Molport, monkeypatch: MonkeyPatch, code, msg
):
    monkeypatch.setattr(
        "cloudscraper.CloudScraper.get",
        lambda *args, **kwargs: MockResponse(code, json_data={}, text=msg),
    )
    with pytest.raises(ValueError) as exc:
        molport.get_suppliers("C1=CC=CC=C1")
    assert msg in str(exc.value)


def test_get_suppliers_bad_format(molport: Molport, monkeypatch: MonkeyPatch):
    monkeypatch.setattr(
        "cloudscraper.CloudScraper.get",
        lambda *args, **kwargs: MockResponse(
            200, json_data={"error": "Invalid response"}
        ),
    )
    with pytest.raises(ValidationError):
        molport.get_suppliers("C1=CC=CC=C1")


def test_get_suppliers_raw_response(
    molport: Molport, supplier_response: ResponseSupplier, monkeypatch: MonkeyPatch
):
    monkeypatch.setattr(
        "cloudscraper.CloudScraper.get",
        lambda *args, **kwargs: MockResponse(
            200, json_data=supplier_response.model_dump(by_alias=True)
        ),
    )
    response = molport.get_suppliers("Molport-000-871-563", return_response=True)
    assert isinstance(response, ResponseSupplier)


@pytest.mark.parametrize(
    "status",
    [0, 1, 2, 3, 4],
)
def test_bad_result_status(molport: Molport, status):
    response = MockResponseSupplier(status=status)
    if response.result.status != ResultStatus.SUCCESS.value:
        with pytest.raises(ValueError) as exc:
            molport.extract_suppliers(response)
        assert str(exc.value) == response.result.message, "Error message is incorrect"


@pytest.mark.parametrize(
    "molport_obj",
    [lazy_fixture("molport"), lazy_fixture("molport_api_key")],
)
def test_extract_suppliers(supplier_response, molport_obj: Molport):
    suppliers = molport_obj.extract_suppliers(supplier_response)
    assert isinstance(suppliers, pd.DataFrame)
    for col in suppliers.columns:
        assert col in [
            "supplier_name",
            "supplier_type",
            "amount",
            "measure",
            "measure_id",
            "price",
            "currency",
            "currency_id",
            "delivery_days",
            "catalog_id",
            "catalog_number",
            "stock",
            "stock_measure",
            "stock_measure_id",
            "purity",
            "last_update_date",
            "last_update_date_exact",
        ], f"Column {col} is not in the DataFrame"
