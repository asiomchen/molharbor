from __future__ import annotations
import pandas as pd
import httpx
from dataclasses import dataclass, field
import logging
from typing import List, Dict, Optional, Union, Iterable
from molharbor.data import Response, ResponseSupplier
from molharbor.exceptions import LoginError, UnknownSearchTypeException
from molharbor.enums import SearchType, ResultStatus
from pydantic import ValidationError


class Molport:
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
        elif username and password:
            self._username = username
            self._password = password
        else:
            raise LoginError(
                "Please provide either username and password or api_key to login"
            )

    def find(
        self,
        smiles: Union[str, Iterable[str]],
        search_type: Union[SearchType, int] = SearchType.EXACT,
        max_results: int = 1000,
        similarity: Optional[float] = 0.9,
        progress_bar: bool = False,
        return_response: bool = False,
    ) -> List[List[MolportCompound] | Response]:
        try:
            search_type = SearchType(search_type)
        except ValueError:
            raise UnknownSearchTypeException(search_type)

        if isinstance(smiles, str):
            smiles = [smiles]
        elif not isinstance(smiles, Iterable):
            raise TypeError(f"Expected str or Iterable[str], got {type(smiles)}")
        if progress_bar and len(smiles) > 1:
            # if jupyter notebook is used, use tqdm.notebook
            if "IPython" in globals():
                from tqdm.notebook import tqdm
            else:
                from tqdm import tqdm
            inputs = tqdm(smiles)
        else:
            inputs = smiles
        result = [
            self._find(
                smiles,
                SearchType(search_type),
                max_results,
                similarity,
                return_response,
            )
            for smiles in inputs
        ]
        return result

    def _find(
        self,
        smiles: str,
        search_type: SearchType,
        max_results: int,
        similarity: Optional[float] = 0.9,
        return_response: bool = False,
    ) -> List[MolportCompound | Response | None]:
        """
        Finds the Molport ID of a compound. If compound have molport ID exists,
         assupms that it is commercial.
        :param smiles: canonical smiles string
        :return:
        """
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
            return [None]
        try:
            response = Response(**similarity_request.json())
            if response.result.status != ResultStatus.SUCCESS.value:
                msg = response.result.message
                if "Username or password is incorrect!" in msg:
                    raise LoginError("Credentials are incorrect, please login again")
                logging.error(msg)
                return [None]
        except ValidationError as e:
            logging.error(e)
            print(e)
            return [None]
        if return_response:
            return response
        mols = response.data.molecules
        if not mols:
            return [None]
        return [MolportCompound(mol.smiles, mol.molport_id) for mol in mols]

    def get_compound_suppliers(
        self, molport_id: str, return_response: bool = True
    ) -> Union[pd.DataFrame, Dict]:
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
            return None


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
