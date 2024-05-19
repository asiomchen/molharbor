from molharbor.exceptions import UnknownSearchTypeException
from molharbor.data import SearchPayload
from molharbor.enums import SearchType
from typing import Dict, Optional, Union


def compound_search_payload(
    smiles: str,
    search_type: Union[SearchType, int] = SearchType.EXACT_FRAGMENT,
    maximum_search_time: Optional[int] = None,
    max_results: int = 10000,
    similarity: float = 0.9,
    credentials: Dict[str, str] = {},
) -> Dict[str, Union[str, int, float]]:
    try:
        search_type = SearchType(search_type)
    except ValueError:
        raise UnknownSearchTypeException(search_type)

    search_payload = SearchPayload(
        smiles=smiles,
        search_type=search_type,
        maximum_search_time=maximum_search_time,
        max_results=max_results,
        similarity=similarity,
        **credentials,
    )
    return search_payload.model_dump(by_alias=True, exclude_none=True)
