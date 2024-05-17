class MockResponse:
    def __init__(self, status_code: int, json_data: dict, text: str = ""):
        self.status_code = status_code
        self.json_data = json_data
        self.text = text

    def json(self) -> dict:
        return self.json_data


class MockResponseSupplier:
    def __init__(self, status: int):
        self.result = MockResult(status)


class MockResult:
    def __init__(self, status: int):
        self.status = status
        self.message = "Error message"
