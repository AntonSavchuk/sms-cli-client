class HTTPRequest:
    def __init__(self, method: str, url: str, header: dict, body: str):
        pass
    
    def to_bytes(self) -> bytes:
        pass

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        pass


class HTTPResponse:
    def __init__(self, status_code: int, headers: dict, body: str):
        pass

    def to_bytes(self) -> bytes:
        pass

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        pass