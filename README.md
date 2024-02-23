
# MolHarbour

MolHarbour is a Python wrapper for the Molport REST API. It allows you to search for chemical compounds and retrieve information about them.
Additionally, MolHarbour unifies the Molport API variables names and verifies the response data using [Pydantic](https://github.com/pydantic/pydantic) models.



## Installation

### From PyPI

```bash
pip install molharbor
```

### From source

```bash
pip install git+https://github.com/asiomchen/pymolport

```

## Quickstart
### Authentication

To start using MolHarbour, you need to create an instance of the `Molport` class and log in to the Molport API using your username and password or API key.

```python
from molharbor.checker import Molport
molport = Molport()
molport.login(username="john.spade", password="fasdga34a3")
```

or API key

```python
molport.login(api_key="16072de6-d318-4324-a82c-08c7dfe64d5d")
```

### Compound search

You can search for compounds using the `search` method. All the search types are supported( via SearchType enum).
Additionally, you can specify the maximum number of results to return using the `max_results` parameter, and the minimum similarity threshold using the `similarity` parameter (is used only for similarity search).


#### Exact search

```python
from molharbor.checker import SearchType
molport.find("O=C(O)c1ccccc1", search_type=SearchType.EXACT)

[[MolportCompound(smiles='OC(=O)c1ccccc1', molport_id='Molport-000-871-563', link='https://www.molport.com/shop/compound/Molport-000-871-563'),
  MolportCompound(smiles='[2H]c1c([2H])c([2H])c(c([2H])c1[2H])C(O)=O', molport_id='Molport-003-927-939', link='https://www.molport.com/shop/compound/Molport-003-927-939'),
  MolportCompound(smiles='O[13C](=O)c1ccccc1', molport_id='Molport-003-929-055', link='https://www.molport.com/shop/compound/Molport-003-929-055'),
  MolportCompound(smiles='OC(=O)[13c]1[13cH][13cH][13cH][13cH][13cH]1', molport_id='Molport-046-688-787', link='https://www.molport.com/shop/compound/Molport-046-688-787')]]

```

#### Similarity search

```python
molport.find("O=C(O)c1ccccc1", search_type=SearchType.SIMILARITY, max_results=5)

[[MolportCompound(smiles='OC(=O)c1ccccc1', molport_id='Molport-000-871-563', link='https://www.molport.com/shop/compound/Molport-000-871-563'),
  MolportCompound(smiles='[2H]c1c([2H])c([2H])c(c([2H])c1[2H])C(O)=O', molport_id='Molport-003-927-939', link='https://www.molport.com/shop/compound/Molport-003-927-939'),
  MolportCompound(smiles='O[13C](=O)c1ccccc1', molport_id='Molport-003-929-055', link='https://www.molport.com/shop/compound/Molport-003-929-055'),
  MolportCompound(smiles='[Zn++].[O-]C(=O)c1ccccc1.[O-]C(=O)c1ccccc1', molport_id='Molport-003-986-949', link='https://www.molport.com/shop/compound/Molport-003-986-949'),
  MolportCompound(smiles='OC(=O)[13c]1[13cH][13cH][13cH][13cH][13cH]1', molport_id='Molport-046-688-787', link='https://www.molport.com/shop/compound/Molport-046-688-787')]]

```

#### Superstructure search

```python

molport.find("O=C(O)c1ccccc1", search_type=SearchType.SUPERSTRUCTURE, max_results=5)

[[MolportCompound(smiles='CC=O', molport_id='Molport-001-783-184', link='https://www.molport.com/shop/compound/Molport-001-783-184'),
  MolportCompound(smiles='OCc1ccccc1', molport_id='Molport-001-783-216', link='https://www.molport.com/shop/compound/Molport-001-783-216'),
  MolportCompound(smiles='C=O', molport_id='Molport-001-785-627', link='https://www.molport.com/shop/compound/Molport-001-785-627'),
  MolportCompound(smiles='CCO', molport_id='Molport-001-785-844', link='https://www.molport.com/shop/compound/Molport-001-785-844'),
  MolportCompound(smiles='O', molport_id='Molport-003-926-090', link='https://www.molport.com/shop/compound/Molport-003-926-090')]]

```

#### Substructure search

```python
molport.find("O=C(O)c1ccccc1", search_type=SearchType.SUBSTRUCTURE, max_results=5)

[[MolportCompound(smiles='OC(=O)c1ccc2[nH]c(S)nc2c1', molport_id='Molport-000-004-519', link='https://www.molport.com/shop/compound/Molport-000-004-519'),
  MolportCompound(smiles='OC(=O)c1cc(C#N)c(Cl)cc1Cl', molport_id='Molport-051-434-827', link='https://www.molport.com/shop/compound/Molport-051-434-827'),
  MolportCompound(smiles='OC(=O)c1ccc(cc1)-c1ccc(cc1)-c1ccc(cc1)N(c1ccc(cc1)-c1ccc(cc1)-c1ccc(cc1)C(O)=O)c1ccc(cc1)-c1ccc(cc1)-c1ccc(cc1)C(O)=O', molport_id='Molport-051-434-831', link='https://www.molport.com/shop/compound/Molport-051-434-831'),
  MolportCompound(smiles='COC(=O)[C@]1(C[C@H](OC(C)=O)[C@@H](NC(C)=O)[C@@H](O1)[C@H](OC(C)=O)[C@@H](COC(C)=O)OC(C)=O)O[C@H]1[C@@H](OC(=O)c2ccccc2)[C@@H](COC(=O)c2ccccc2)O[C@@H](Oc2ccc(OC)cc2)[C@@H]1OC(=O)c1ccccc1', molport_id='Molport-051-434-926', link='https://www.molport.com/shop/compound/Molport-051-434-926'),
  MolportCompound(smiles='[Na+].[Na+].OC(=O)CN(CC([O-])=O)Cc1cc2c(Oc3cc(O)c(CN(CC(O)=O)CC([O-])=O)cc3C22OC(=O)c3ccccc23)cc1O', molport_id='Molport-051-435-130', link='https://www.molport.com/shop/compound/Molport-051-435-130')]]

```
