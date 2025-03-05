class MockResponse:
    """Mocking the response object from `httpx` library.

    Args:
        status_code (int): status code of the response
        json_data (dict): json data of the response would be returned by .json() method
        text (str, optional): text of the response. Defaults to "".
    """

    def __init__(self, status_code: int, json_data: dict, text: str = ""):
        self.status_code = status_code
        self.json_data = json_data
        self.text = text

    def json(self) -> dict:
        return self.json_data

    def raise_for_status(self):
        if self.status_code != 200:
            raise ValueError(f"Error code: {self.status_code}\n{self.text}")


class MockResponseSupplier:
    """Mocking the ResponseSupplier object from molharbor.data module.

    Args:
        status (int): status of the response available in as `.result.status` attribute
    """

    def __init__(self, status: int):
        self.result = MockResult(status)


class MockResult:
    def __init__(self, status: int):
        self.status = status
        self.message = "Error message"
