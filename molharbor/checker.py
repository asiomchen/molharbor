from __future__ import annotations
import pandas as pd
import httpx
from dataclasses import dataclass, field
import logging
from typing import List, Optional, Union
from molharbor.data import Response, ResponseSupplier
from molharbor.exceptions import LoginError
from molharbor.enums import SearchType, ResultStatus
from molharbor.utils import compound_search_payload
from pydantic import ValidationError


class Molport:
    __slots__ = ["client", "_api_key", "_username", "_password"]

    def __init__(self):
        self.client = httpx.Client()
        self._api_key = None
        self._username = None
        self._password = None

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    @property
    def credentials(self):
        if self.api_key:
            return {"api_key": self.api_key}
        elif self.username and self.password:
            return {"username": self.username, "password": self.password}
        else:
            raise LoginError(
                "No credentials are provided. Please login with username and password or api_key using .login()"
            )

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, value):
        self._api_key = value
        print("API key is set and will be used as default for all requests")
        self._username = None
        self._password = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        self._username = value

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, value):
        self._password = value

    def login(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ):
        """
        Login to Molport API. If api_key is provided, it will be used as default for all requests.
        """
        if all([username, password, api_key]):
            raise LoginError("Please provide either username and password or api_key")
        elif api_key:
            self._api_key = api_key
            self._username = None
            self._password = None
        elif username and password:
            self._username = username
            self._password = password
            self._api_key = None
        else:
            raise LoginError(
                "Please provide either username and password or api_key to login"
            )

    def find(
        self,
        /,
        smiles: str,
        *,
        search_type: Union[SearchType, int] = SearchType.EXACT_FRAGMENT,
        max_search_time: Optional[int] = None,
        max_results: int = 10000,
        similarity: float = 0.9,
        return_response: bool = False,
    ) -> List[MolportCompound] | Response:
        """Find compounds by SMILES string in Molport database, have the same default values as the API

        Args:
            smiles (str): SMILES string of the compound
            search_type (Union[SearchType, int], optional): _description_. Defaults to SearchType.EXACT_FRAGMENT.
            max_search_time (Optional[int], optional): time in miliseconds - maximum search time to be spent on chemical search
            max_results (int, optional): maximum result count which must be returned as result; currently maximum allowed value is 10000. Defaults to 10000.
            similarity (float, optional): if similarity search is made, it is possible to provide similarity index in range 0 - 1. Defaults to 0.9.
            return_response (bool, optional): If True, returns the response object. Otherwise parses the response and returns a list of `MolportCompound` objects. Defaults to False.

        Raises:
            TypeError: If SMILES is not a string
            LoginError: If credentials are incorrect
            ValidationError: If the response or payload is not valid

        Returns:
            List[MolportCompound] | Response: List of MolportCompound objects or Response object
        """
        if not isinstance(smiles, str):
            raise TypeError("SMILES must be a string")
        payload = compound_search_payload(
            smiles=smiles,
            search_type=search_type,
            maximum_search_time=max_search_time,
            max_results=max_results,
            similarity=similarity,
            credentials=self.credentials,
        )
        similarity_request = self.client.post(
            "https://api.molport.com/api/chemical-search/search", json=payload
        )
        if similarity_request.status_code != 200:
            logging.error(f"Error code: {similarity_request.status_code}")
            return []
        try:
            response = Response(**similarity_request.json())
            if response.result.status != ResultStatus.SUCCESS.value:
                msg = response.result.message
                if "Username or password is incorrect!" in msg:
                    raise LoginError("Credentials are incorrect, please login again")
                logging.error(msg)
                return []
        except ValidationError as e:
            logging.error(e)
            return []
        if return_response:
            return response
        mols = response.data.molecules
        if not mols:
            return []
        return [MolportCompound(mol.smiles, mol.molport_id) for mol in mols]

    def get_suppliers(
        self, molport_id: str, return_response: bool = False
    ) -> Union[pd.DataFrame, ResponseSupplier]:
        """Get suppliers for a given Molport ID

        Args:
            molport_id (str): Molport ID of the compound
            return_response (bool, optional): If True, returns the response object. Otherwise parses the response and returns a DataFrame. Defaults to False.

        Raises:
            ValueError: If the response status is not 200

        Returns:
            Union[pd.DataFrame, ResponseSupplier]: DataFrame with supplier information or Response object
        """
        credentials = self.credentials
        url = "https://api.molport.com/api/molecule/load?molecule={}"
        if "api_key" in credentials:
            url += "&apikey={}"
            url = url.format(molport_id, credentials["api_key"])
        else:
            url += "&username={}&authenticationcode={}"
            url = url.format(molport_id, self.username, self.password)
        response = self.client.get(url)
        if response.status_code != 200:
            raise ValueError(f"Error code: {response.status_code}\n{response.text}")
        data = ResponseSupplier(**response.json())
        if return_response:
            return data
        else:
            return self.extract_suppliers(data)

    def extract_suppliers(self, response: ResponseSupplier) -> pd.DataFrame:
        """Extract suppliers from the response data

        Args:
            response (ResponseSupplier): Response data from the API

        Raises:
            ValueError: If the response status is not SUCCESS

        Returns:
            pd.DataFrame: DataFrame with supplier information
        """
        if response.result.status != ResultStatus.SUCCESS.value:
            raise ValueError(response.result.message)
        types = [
            "screening_block_suppliers",
            "building_block_suppliers",
            "virtual_suppliers",
        ]
        records = []
        for supp_type in types:
            if hasattr(response.data.molecule.catalogues, supp_type):
                for supp in response.data.molecule.catalogues.screening_block_suppliers:
                    for catalog in supp.catalogues:
                        data = catalog.model_dump()
                        packings = data.pop("available_packings")
                        name = {
                            "supplier_name": supp.supplier_name,
                            "supplier_type": supp_type,
                        }
                        for packing in packings:
                            record = {**name, **packing, **data}
                            records.append(record)
        df = pd.DataFrame(records)
        return df


@dataclass
class MolportCompound:
    smiles: str
    molport_id: str
    link: str = field(init=False)

    def __post_init__(self):
        self.link = (
            f"https://www.molport.com/shop/compound/{self.molport_id}"
            if self.molport_id
            else ""
        )
