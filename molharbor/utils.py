from molharbor.exceptions import UnknownSearchTypeException
from molharbor.enums import SearchType
from typing import Dict, Union


def compound_search_payload(
    smiles: str,
    search_type: Union[SearchType, int],
    max_results: int,
    similarity: float,
    credentials: Dict[str, str],
) -> Dict[str, Union[str, int, float]]:
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
    payload.update(credentials)
    return payload
