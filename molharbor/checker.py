from __future__ import annotations
import pandas as pd
import httpx
from dataclasses import dataclass, field
import logging
from typing import List, Optional, Union
from molharbor.data import Response, ResponseSupplier
from molharbor.exceptions import LoginError, UnknownSearchTypeException
from molharbor.enums import SearchType, ResultStatus
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
            return {"API Key": self.api_key}
        elif self.username and self.password:
            return {"User Name": self.username, "Authentication Code": self.password}
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
        smiles: str,
        search_type: Union[SearchType, int] = SearchType.EXACT,
        max_results: int = 1000,
        similarity: float = 0.9,
        return_response: bool = False,
    ) -> List[MolportCompound] | Response:
        if not isinstance(smiles, str):
            raise TypeError("SMILES must be a string")
        try:
            search_type = SearchType(search_type)
        except ValueError:
            raise UnknownSearchTypeException(search_type)
        payload = {
            "Structure": smiles,
            "Search Type": search_type.value,
            "Maximum Search Time": 60000,
            "Maximum Result Count": max_results,
            "Chemical Similarity Index": similarity,
        }
        creds = self.credentials
        payload.update(creds)
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
            print(e)
            return []
        if return_response:
            return response
        mols = response.data.molecules
        if not mols:
            return []
        return [MolportCompound(mol.smiles, mol.molport_id) for mol in mols]

    def get_compound_suppliers(
        self, molport_id: str, return_response: bool = False
    ) -> Union[pd.DataFrame, ResponseSupplier]:
        credentials = self.credentials
        url = "https://api.molport.com/api/molecule/load?molecule={}"
        if "API Key" in credentials:
            url += "&apikey={}"
            url = url.format(molport_id, self.api_key)
        else:
            url += "&username={}&password={}"
            url = url.format(molport_id, self.username, self.password)

        response = self.client.get(url)
        if return_response:
            return ResponseSupplier(**response.json())
        else:
            return self.extract_suppliers(ResponseSupplier(**response.json()))

    def extract_suppliers(self, response: ResponseSupplier) -> pd.DataFrame:
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
