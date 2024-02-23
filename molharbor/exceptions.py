from molharbor.enums import SearchType
from typing import Union


class UnknownSearchTypeException(ValueError):
    """Exception raised when an unknown search type is specified."""

    def __init__(self, search_type: Union[SearchType, int]) -> None:
        self.search_type = search_type
        super().__init__(
            f"Unknown search type: {search_type}. Expected one of: {list(SearchType)}"
        )


class LoginError(Exception):
    """Exception raised when login fails."""

    pass
