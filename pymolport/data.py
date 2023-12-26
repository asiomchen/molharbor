from typing import List, Optional
from pydantic import BaseModel, Field
import numpy as np


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
    currency: str = Field(alias="currency")
    currency_id: int = Field(alias="Currency Id")
    delivery_days: int = Field(alias="Delivery Days")


class Catalog(BaseModel):
    Catalog_Id: int = Field(alias="Catalog Id")
    Catalog_Number: str = Field(alias="Catalog Number")
    Stock: Optional[float] = Field(None, alias="Stock")
    Stock_Measure: Optional[str] = Field(None, alias="Stock Measure")
    Stock_Measure_Id: Optional[int] = Field(None, alias="Stock Measure Id")
    Purity: str = Field("unknown", alias="Purity")
    Last_Update_Date: str = Field(alias="Last Update Date")
    Last_Update_Date_Exact: str = Field(alias="Last Update Date Exact")
    Available_Packings: List[AvailablePacking] = Field(alias="Available Packings")


class Supplier(BaseModel):
    Supplier_Name: str = Field(alias="Supplier Name")
    Supplier_Id: int = Field(alias="Supplier Id")
    Minimum_Order: int = Field(alias="Minimum Order")
    Currency: str
    Currency_Id: int = Field(alias="Currency Id")
    Catalogues: List[Catalog]


class BagOfSuppliers(BaseModel):
    Screening_Block_Suppliers: Optional[List[Supplier]] = Field(
        alias="Screening Block Suppliers"
    )
    Building_Block_Suppliers: Optional[List[Supplier]] = Field(
        alias="Building Block Suppliers"
    )
    Virtual_Suppliers: Optional[List[Supplier]] = Field(alias="Virtual Suppliers")


class ShipmentCost(BaseModel):
    Price: float
    Currency: str
    Currency_Id: int = Field(alias="Currency Id")
    Location_Type: str = Field(alias="Location Type")
    Location: str
    Location_Id: int = Field(alias="Location Id")
    Shipment_Type: str = Field(alias="Shipment Type")
    Shipment_Type_Id: int = Field(alias="Shipment Type Id")


class Molecule2(BaseModel):
    Id: int = Field(..., alias="Id")
    Molport_Id: str = Field(..., alias="Molport Id")
    SMILES: str = Field(..., alias="SMILES")
    Canonical_SMILES: str = Field(..., alias="Canonical SMILES")
    IUPAC: str
    Formula: str
    Molecular_Weight: float = Field(..., alias="Molecular Weight")
    Status: str
    Type: str
    Largest_Stock: str = Field(..., alias="Largest Stock")
    Largest_Stock_Measure: str = Field(..., alias="Largest Stock Measure")
    Largest_Stock_Measure_Id: int = Field(..., alias="Largest Stock Measure Id")
    Catalogues: BagOfSuppliers = Field(..., alias="Catalogues")
    Synonyms: List[str]


class DataSupplier(BaseModel):
    molecule: Molecule2 = Field(alias="Molecule")
    version: str = Field(alias="Version")


class ResponseSupplier(Response):
    data: DataSupplier = Field(alias="Data")
