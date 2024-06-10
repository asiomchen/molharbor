
# MolHarbour
[![image](https://shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue)](#)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![codecov](https://codecov.io/gh/asiomchen/molharbor/graph/badge.svg?token=BPMQ6F3IV9)](https://codecov.io/gh/asiomchen/molharbor)

MolHarbour is a unofficial Python wrapper for the Molport REST API. It allows you to search for chemical compounds and retrieve information about them.
Additionally, MolHarbour unifies the Molport API variables names and verifies the response data using wonderful [Pydantic](https://github.com/pydantic/pydantic) models.

This library is not affiliated with Molport in any way. Molport is a registered trademark of Molport SIA.

The project was initiated as a part of my master's thesis and and is based on refactored scripts which I wrote to retrive commercial availablity of compounds in chembl database.

## Installation

### From PyPI

```bash
pip install molharbor
```

### From source

```bash
pip install git+https://github.com/asiomchen/molharbor

```

## Quickstart
### Authentication

To start using MolHarbour, you need to create an instance of the `Molport` class and log in to the Molport API using your username and password or API key.

```python
from molharbor import Molport
molport = Molport()
molport.login(username="john.spade", password="fasdga34a3")
```

or API key

```python
molport.login(api_key="16072de6-d318-4324-a82c-08c7dfe64d5d")
```

### Compound search

You can search for compounds using the `search` method. All the search types are supported( via `SearchType` enum).
Additionally, you can specify the maximum number of results to return using the `max_results` parameter, and the minimum similarity threshold using the `similarity` parameter (it is used only for similarity search).


#### Exact search

```python
from molharbor import SearchType
molport.find("O=C(O)c1ccccc1", search_type=SearchType.EXACT)

[[MolportCompound(smiles='OC(=O)c1ccccc1', molport_id='Molport-000-871-563', link='https://www.molport.com/shop/compound/Molport-000-871-563'),
  MolportCompound(smiles='[2H]c1c([2H])c([2H])c(c([2H])c1[2H])C(O)=O', molport_id='Molport-003-927-939', link='https://www.molport.com/shop/compound/Molport-003-927-939'),
  MolportCompound(smiles='O[13C](=O)c1ccccc1', molport_id='Molport-003-929-055', link='https://www.molport.com/shop/compound/Molport-003-929-055'),
  MolportCompound(smiles='OC(=O)[13c]1[13cH][13cH][13cH][13cH][13cH]1', molport_id='Molport-046-688-787', link='https://www.molport.com/shop/compound/Molport-046-688-787')]]

```

#### Similarity search

```python
molport.find("O=C(O)c1ccccc1", 
              search_type=SearchType.SIMILARITY, 
              max_results=5)

[[MolportCompound(smiles='OC(=O)c1ccccc1', molport_id='Molport-000-871-563', link='https://www.molport.com/shop/compound/Molport-000-871-563'),
  MolportCompound(smiles='[2H]c1c([2H])c([2H])c(c([2H])c1[2H])C(O)=O', molport_id='Molport-003-927-939', link='https://www.molport.com/shop/compound/Molport-003-927-939'),
  MolportCompound(smiles='O[13C](=O)c1ccccc1', molport_id='Molport-003-929-055', link='https://www.molport.com/shop/compound/Molport-003-929-055'),
  MolportCompound(smiles='[Zn++].[O-]C(=O)c1ccccc1.[O-]C(=O)c1ccccc1', molport_id='Molport-003-986-949', link='https://www.molport.com/shop/compound/Molport-003-986-949'),
  MolportCompound(smiles='OC(=O)[13c]1[13cH][13cH][13cH][13cH][13cH]1', molport_id='Molport-046-688-787', link='https://www.molport.com/shop/compound/Molport-046-688-787')]]

```

#### Superstructure search

```python

molport.find("O=C(O)c1ccccc1", 
              search_type=SearchType.SUPERSTRUCTURE, 
              max_results=5)

[[MolportCompound(smiles='CC=O', molport_id='Molport-001-783-184', link='https://www.molport.com/shop/compound/Molport-001-783-184'),
  MolportCompound(smiles='OCc1ccccc1', molport_id='Molport-001-783-216', link='https://www.molport.com/shop/compound/Molport-001-783-216'),
  MolportCompound(smiles='C=O', molport_id='Molport-001-785-627', link='https://www.molport.com/shop/compound/Molport-001-785-627'),
  MolportCompound(smiles='CCO', molport_id='Molport-001-785-844', link='https://www.molport.com/shop/compound/Molport-001-785-844'),
  MolportCompound(smiles='O', molport_id='Molport-003-926-090', link='https://www.molport.com/shop/compound/Molport-003-926-090')]]

```

#### Substructure search

```python
molport.find("O=C(O)c1ccccc1", 
              search_type=SearchType.SUBSTRUCTURE, 
              max_results=5)

[[MolportCompound(smiles='OC(=O)c1ccc2[nH]c(S)nc2c1', molport_id='Molport-000-004-519', link='https://www.molport.com/shop/compound/Molport-000-004-519'),
  MolportCompound(smiles='OC(=O)c1cc(C#N)c(Cl)cc1Cl', molport_id='Molport-051-434-827', link='https://www.molport.com/shop/compound/Molport-051-434-827'),
  MolportCompound(smiles='OC(=O)c1ccc(cc1)-c1ccc(cc1)-c1ccc(cc1)N(c1ccc(cc1)-c1ccc(cc1)-c1ccc(cc1)C(O)=O)c1ccc(cc1)-c1ccc(cc1)-c1ccc(cc1)C(O)=O', molport_id='Molport-051-434-831', link='https://www.molport.com/shop/compound/Molport-051-434-831'),
  MolportCompound(smiles='COC(=O)[C@]1(C[C@H](OC(C)=O)[C@@H](NC(C)=O)[C@@H](O1)[C@H](OC(C)=O)[C@@H](COC(C)=O)OC(C)=O)O[C@H]1[C@@H](OC(=O)c2ccccc2)[C@@H](COC(=O)c2ccccc2)O[C@@H](Oc2ccc(OC)cc2)[C@@H]1OC(=O)c1ccccc1', molport_id='Molport-051-434-926', link='https://www.molport.com/shop/compound/Molport-051-434-926'),
  MolportCompound(smiles='[Na+].[Na+].OC(=O)CN(CC([O-])=O)Cc1cc2c(Oc3cc(O)c(CN(CC(O)=O)CC([O-])=O)cc3C22OC(=O)c3ccccc23)cc1O', molport_id='Molport-051-435-130', link='https://www.molport.com/shop/compound/Molport-051-435-130')]]

```

#### Raw response manipulation

MolHarbour design to simplify commonn tasks so `.find()` method returns a list of `MolportCompound` objects (which itself is a dataclass object with `smiles`, `molport_id` and `link` field). 

However, you can access the raw response using the `return_response` parameter. Returned `Response` object inherits from Pydantic `BaseModel` and contains all the fields from the Molport API response with type validation provided by Pydantic.
All the fields have the same name as in Molport API docs, only lowercase and the spaces are replaced with underscores( e.g. `Shipment Type` -> `shipment_type`)

```python
from molharbor import SearchType
molport.find("O=C(O)c1ccccc1", 
              search_type=SearchType.SUBSTRUCTURE, 
              max_results=1, 
              return_response=False)

[[MolportCompound(smiles='OC(=O)c1cc(C#N)c(Cl)cc1Cl', molport_id='Molport-051-434-827', link='https://www.molport.com/shop/compound/Molport-051-434-827')]]
```
vs

```python
molport.find("O=C(O)c1ccccc1", 
              search_type=SearchType.SUBSTRUCTURE, 
              max_results=1, 
              return_response=True)

[Response(result=Result(status=1, message='Substructure search completed!'), data=Data(molecules=[Molecule(id=45........
```

### Suppliers search

Having a Molport ID, you can search for suppliers using the `get_suppliers` method. Similar too `find()` method, you could either recieve a raw pydantic response with all the fields having the same name as in Molport API docs, only lowercase and the spaces are replaced with underscores( e.g. `Shipment Type` -> `shipment_type`) or processed dataframe with most important fields

```python
df = molport.get_suppliers("Molport-001-794-639")
```

Or you could use id values of `MolportCompound` objects returned by `find()` method

```python
result = molport.find("C[C@H](CS)C(=O)N1CCC[C@H]1C(O)=O", search_type=SearchType.EXACT, max_results=1)[0]
result

MolportCompound(smiles='C[C@H](CS)C(=O)N1CCC[C@H]1C(O)=O', molport_id='Molport-001-794-639', link=...

df = molport.get_suppliers(result.molport_id)
```
#### Processed dataframe

Returned dataframe contains all the fields from the Molport API response with type validation provided by Pydantic. The fields are renamed to be more human-readable and to be consistent with the Molport API docs. Below is an example of the most important fields.

```python
df[["supplier_name", "supplier_type", "amount", "measure", 
"price", "currency", "delivery_days", 
"stock", "stock_measure", "last_update_date_exact"]].head()
```
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>supplier_name</th>
      <th>supplier_type</th>
      <th>amount</th>
      <th>measure</th>
      <th>price</th>
      <th>currency</th>
      <th>delivery_days</th>
      <th>stock</th>
      <th>stock_measure</th>
      <th>last_update_date_exact</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>BIONET - Key Organics Ltd.</td>
      <td>screening_block_suppliers</td>
      <td>1.0</td>
      <td>mg</td>
      <td>45.0</td>
      <td>USD</td>
      <td>4</td>
      <td>1187.6</td>
      <td>mg</td>
      <td>May 17, 2024</td>
    </tr>
    <tr>
      <th>1</th>
      <td>BIONET - Key Organics Ltd.</td>
      <td>screening_block_suppliers</td>
      <td>5.0</td>
      <td>mg</td>
      <td>53.0</td>
      <td>USD</td>
      <td>4</td>
      <td>1187.6</td>
      <td>mg</td>
      <td>May 17, 2024</td>
    </tr>
    <tr>
      <th>2</th>
      <td>BIONET - Key Organics Ltd.</td>
      <td>screening_block_suppliers</td>
      <td>10.0</td>
      <td>mg</td>
      <td>64.0</td>
      <td>USD</td>
      <td>4</td>
      <td>1187.6</td>
      <td>mg</td>
      <td>May 17, 2024</td>
    </tr>
    <tr>
      <th>3</th>
      <td>BIONET - Key Organics Ltd.</td>
      <td>screening_block_suppliers</td>
      <td>1.0</td>
      <td>mg</td>
      <td>45.0</td>
      <td>USD</td>
      <td>4</td>
      <td>1187.6</td>
      <td>mg</td>
      <td>May 17, 2024</td>
    </tr>
    <tr>
      <th>4</th>
      <td>BIONET - Key Organics Ltd.</td>
      <td>screening_block_suppliers</td>
      <td>2.0</td>
      <td>mg</td>
      <td>47.0</td>
      <td>USD</td>
      <td>4</td>
      <td>1187.6</td>
      <td>mg</td>
      <td>May 17, 2024</td>
    </tr>
  </tbody>
</table>

#### Raw response

```python
molport.get_suppliers("Molport-000-871-563", return_response=True)

ResponseSupplier(result=Result(status=1, message='Molecule found!'), data=DataSupplier(molecule=Molecule2(id=871563, molport_id='Molport-000-871-563', smiles='OC(=O)c1ccccc1', .....
```
