from typing import List, Optional
from pydantic_core import PydanticCustomError
from pydantic import BaseModel, ConfigDict, Field, model_validator
import numpy as np
from molharbor.enums import SearchType


class Molecule(BaseModel):
    id: int = Field(..., alias="Id")
    molport_id: str = Field(..., alias="MolPort Id")
    smiles: str = Field(None, alias="SMILES")
    canonical_smiles: str = Field(None, alias="Canonical SMILES")
    verified_amount: float = Field(None, alias="Verified Amount")
    unverified_amount: float = Field(None, alias="Unverified Amount")
    similarity_index: float = Field(None, alias="Similarity Index")


class Data(BaseModel):
    molecules: Optional[List[Molecule]] = Field(alias="Molecules")
    version: str = Field(alias="Version")


class Result(BaseModel):
    status: int = Field(alias="Status")
    message: str = Field(alias="Message")


class Response(BaseModel):
    result: Result = Field(alias="Result")
    data: Data = Field(alias="Data")


class AvailablePacking(BaseModel):
    amount: float = Field(np.nan, alias="Amount")
    measure: str = Field(alias="Measure")
    measure_id: int = Field(alias="Measure Id")
    price: float = Field(alias="Price")
    currency: str = Field(alias="Currency")
    currency_id: int = Field(alias="Currency Id")
    delivery_days: int = Field(alias="Delivery Days")


class Catalog(BaseModel):
    catalog_id: int = Field(alias="Catalog Id")
    catalog_number: str = Field(alias="Catalog Number")
    stock: Optional[float] = Field(None, alias="Stock")
    stock_measure: Optional[str] = Field(None, alias="Stock Measure")
    stock_measure_id: Optional[int] = Field(None, alias="Stock Measure Id")
    purity: str = Field("unknown", alias="Purity")
    last_update_date: str = Field(alias="Last Update Date")
    last_update_date_exact: str = Field(alias="Last Update Date Exact")
    available_packings: List[AvailablePacking] = Field(alias="Available Packings")


class Supplier(BaseModel):
    supplier_name: str = Field(alias="Supplier Name")
    supplier_id: int = Field(alias="Supplier Id")
    minimum_order: int = Field(alias="Minimum Order")
    currency: str = Field(alias="Currency")
    currency_id: int = Field(alias="Currency Id")
    catalogues: List[Catalog] = Field(alias="Catalogues")


class BagOfSuppliers(BaseModel):
    screening_block_suppliers: Optional[List[Supplier]] = Field(
        alias="Screening Block Suppliers"
    )
    building_block_suppliers: Optional[List[Supplier]] = Field(
        alias="Building Block Suppliers"
    )
    virtual_suppliers: Optional[List[Supplier]] = Field(alias="Virtual Suppliers")


class ShipmentCost(BaseModel):
    price: float = Field(alias="Price")
    currency: str = Field(alias="Currency")
    currency_Id: int = Field(alias="Currency Id")
    location_Type: str = Field(alias="Location Type")
    location: str = Field(alias="Location")
    location_id: int = Field(alias="Location Id")
    shipment_type: str = Field(alias="Shipment Type")
    shipment_type_id: int = Field(alias="Shipment Type Id")


class Molecule2(BaseModel):
    id: int = Field(..., alias="Id")
    molport_id: str = Field(..., alias="Molport Id")
    smiles: str = Field(..., alias="SMILES")
    canonical_smiles: str = Field(..., alias="Canonical SMILES")
    iupac: str = Field(..., alias="IUPAC")
    formula: str = Field(..., alias="Formula")
    molecular_weight: float = Field(..., alias="Molecular Weight")
    status: str = Field(..., alias="Status")
    type: str = Field(..., alias="Type")
    targest_stock: str = Field(..., alias="Largest Stock")
    largest_stock_measure: str = Field(..., alias="Largest Stock Measure")
    largest_stock_measure_id: int = Field(..., alias="Largest Stock Measure Id")
    catalogues: BagOfSuppliers = Field(..., alias="Catalogues")
    synonyms: List[str] = Field(..., alias="Synonyms")


class DataSupplier(BaseModel):
    molecule: Molecule2 = Field(None, alias="Molecule")
    version: str = Field(alias="Version")


class ResponseSupplier(Response):
    data: DataSupplier = Field(alias="Data")


class SearchPayload(BaseModel):
    smiles: str = Field(..., serialization_alias="Structure")
    search_type: SearchType = Field(
        SearchType.EXACT_FRAGMENT, serialization_alias="Search Type"
    )
    maximum_search_time: Optional[int] = Field(
        None, serialization_alias="Maximum Search Time"
    )
    max_results: int = Field(10000, serialization_alias="Maximum Result Count")
    similarity: float = Field(0.9, serialization_alias="Chemical Similarity Index")
    api_key: Optional[str] = Field(None, serialization_alias="API Key")
    username: Optional[str] = Field(None, serialization_alias="User Name")
    password: Optional[str] = Field(None, serialization_alias="Authentication Code")
    model_config = ConfigDict(use_enum_values=True)

    @model_validator(mode="before")
    def check_auth(cls, values: dict):
        api_key, username, password = (
            values.get("api_key"),
            values.get("username"),
            values.get("password"),
        )
        if api_key:
            values.pop("username", None)
            values.pop("password", None)
            return values
        elif not all((username, password)):
            raise PydanticCustomError(
                "Either username and password or api_key must be provided",
                f"Wrong credintials combination: api_key={api_key}, username={username}, password={password}",
            )
        values.pop("api_key", None)
        return values
