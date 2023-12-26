from __future__ import annotations
import pandas as pd
import httpx
from dataclasses import dataclass, field
import logging
from typing import List, Dict, Optional, Union, Iterable
from pymolport.data import Response
from pymolport.exceptions import LoginError, UnknownSearchTypeException
from pymolport.enums import SearchType, ResultStatus
from pydantic import ValidationError


class Molport:
    def __init__(self):
        self.client = httpx.Client()
        self._api_key = None
        self._username = None
        self._password = None
        # i don't know if this is a good idea, but credentials from the docs are here and working
        self.login(username="john.spade", password="fasdga34a3")

    def __repr__(self) -> str:
        return type(self).__name__ + "()"

    @property
    def credentials(self):
        if self.api_key:
            return {"API Key": self.api_key}
        elif self.username and self.password:
            return {"User Name": self.username, "Authentication Code": self.password}
        else:
            raise ValueError(
                "No credentials provided are set, please set api_key or username and password with login()"
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
            raise LoginError("Please provide either username and password or api_key")

    def find(
        self,
        smiles: Union[str, Iterable[str]],
        search_type: Union[SearchType, int] = SearchType.EXACT,
        max_results: int = 1000,
        similarity: Optional[float] = 0.9,
    ) -> List[List[MolportCompound]]:
        try:
            search_type = SearchType(search_type)
        except ValueError:
            raise UnknownSearchTypeException(search_type)

        if isinstance(smiles, str):
            smiles = [smiles]
        if isinstance(smiles, Iterable):
            return [
                self._find(s, SearchType(search_type), max_results, similarity)
                for s in smiles
            ]
        else:
            raise TypeError(f"Expected str or Iterable[str], got {type(smiles)}")

    def _find(
        self,
        smiles: str,
        search_type: SearchType,
        max_results: int,
        similarity: Optional[float] = 0.9,
    ) -> List[MolportCompound]:
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
            return None
        try:
            response = Response(**similarity_request.json())
            if response.result.status != ResultStatus.SUCCESS.value:
                logging.error(response.result.message)
                return None
        except ValidationError as e:
            logging.error(e)
            print(e)
            return None
        print(response)
        mols = response.data.molecules
        if not mols:
            return None
        return [MolportCompound(mol.smiles, mol.molport_id) for mol in mols]

    def get_compound_suppliers(
        self, molport_id: str, as_df: bool = True
    ) -> Union[pd.DataFrame, Dict]:
        molport_id_request = (
            "https://api.molport.com/api/molecule/load?"
            "molecule={}"
            "&username=john.spade"
            "&authenticationcode=fasdga34a3"
        )
        r2 = self.client.get(molport_id_request.format(molport_id))
        response = r2.json()
        results = response["Data"]["Molecule"]["Catalogues"][
            "Screening Block Suppliers"
        ]
        if as_df:
            df = pd.DataFrame()
            for supplier in results:
                df = df.append(supplier, ignore_index=True)
            shipping_options = pd.DataFrame()
            for s_cost, supplier in zip(df["Shipment Costs"], df["Supplier Name"]):
                shipping_option = pd.DataFrame(
                    s_cost, index=[supplier for i in range(len(s_cost))]
                )
                shipping_options = shipping_options.append(shipping_option)
            catalogs = pd.DataFrame()
            for s_cost, supplier in zip(df["Catalogues"], df["Supplier Name"]):
                catalog = pd.DataFrame(
                    s_cost, index=[supplier for i in range(len(s_cost))]
                )
                catalogs = catalogs.append(catalog)

            merged = pd.merge(
                shipping_options,
                catalogs,
                left_index=True,
                right_index=True,
            )
            return merged
        else:
            return results


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
