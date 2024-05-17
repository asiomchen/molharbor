class MockResponse:
    def __init__(self, status_code: int, json_data: dict):
        self.status_code = status_code
        self.json_data = json_data

    def json(self) -> dict:
        return self.json_data
