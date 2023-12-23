from __future__ import annotations
import pandas as pd
import httpx
from dataclasses import dataclass, field
import logging
from typing import List, Dict, Union, Iterable

class Molport:
    username = "john.spade"
    password = "fasdga34a3"
    def __init__(self):
        self.payload = {
            "User Name": self.username,
            "Authentication Code": self.password,
            "Structure": None,
            "Search Type": "EXACT",
            "Maximum Search Time": 60000,
            "Maximum Result Count": 1000,
            "Chemical Similarity Index": 0.9
        }
        self.client = httpx.Client()
        
    def __repr__(self) -> str:
        return type(self).__name__ + '()'
    
    def find(self, smiles: Union[str, Iterable[str]]) -> List[MolportCompound]:
        """
        Finds the Molport ID of a compound. If compound have molport ID exists,
         assupms that it is commercial.
        :param smiles: canonical smiles string
        :return:
        """
        if isinstance(smiles, str):
            smiles = [smiles]
        if isinstance(smiles, Iterable):
            return [self._find(s) for s in smiles]
        else:
            raise TypeError(f"Expected str or Iterable[str], got {type(smiles)}")
    


    def _find(self, smiles: str) -> MolportCompound:
        """
        Finds the Molport ID of a compound. If compound have molport ID exists,
         assupms that it is commercial.
        :param smiles: canonical smiles string
        :return:
        """
        payload = {
           "User Name": self.username,
           "Authentication Code": self.password,
           "Structure": smiles,
           "Search Type": 4,
           "Maximum Search Time": 60000,
           "Maximum Result Count": 10000,
           "Chemical Similarity Index": 1
        }
        similarity_request = self.client.post('https://api.molport.com/api/chemical-search/search', json=payload)
        response = similarity_request.json()
        try:
            self.molport_id = response['Data']['Molecules'][0]['MolPort Id'][8:]
            logging.debug(f'Molport ID: {self.molport_id}')
            self.is_commercial = True
        except:
            self.molport_id = None
            self.is_commercial = False
        return MolportCompound(smiles, self.molport_id, self.is_commercial)


    def get_compound_suppliers(self, molport_id: str, as_df: bool = True) -> Union[pd.DataFrame, Dict]:
        molport_id_request = 'https://api.molport.com/api/molecule/load?' \
                             'molecule={}' \
                             '&username=john.spade' \
                             '&authenticationcode=fasdga34a3'
        r2 = self.client.get(molport_id_request.format(molport_id))
        response = r2.json()
        results = response['Data']['Molecule']['Catalogues']['Screening Block Suppliers']
        if as_df:
            df = pd.DataFrame()
            for supplier in results:
                df = df.append(supplier, ignore_index=True)
            shipping_options = pd.DataFrame()
            for s_cost, supplier in zip(df['Shipment Costs'], df['Supplier Name']):
                shipping_option = pd.DataFrame(s_cost, index=[supplier for i in range(len(s_cost))])
                shipping_options = shipping_options.append(shipping_option)
            catalogs = pd.DataFrame()
            for s_cost, supplier in zip(df['Catalogues'], df['Supplier Name']):
                catalog = pd.DataFrame(s_cost, index=[supplier for i in range(len(s_cost))])
                catalogs = catalogs.append(catalog)

            merged = pd.merge(shipping_options, catalogs, left_index=True, right_index=True, )
            return merged
        else:
            return results



@dataclass
class MolportCompound:
    smiles: str
    molport_id: str
    commercial: bool
    link: str = field(init=False)

    def __post_init__(self):
        self.link = f'https://www.molport.com/shop/compound/Molport-{self.molport_id}' if self.molport_id else ""