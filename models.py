class HTTPRequest:
    def __init__(self, method: str, url: str, headers: dict, body: str):
        self.method = method
        self.url = url
        self.headers = headers
        self.body = body
    
    def to_bytes(self) -> bytes:
        request_line = f"{self.method} {self.url} HTTP/1.1\r\n"
        headers = "".join(f"{k}: {v}\r\n" for k, v in self.headers.items())
        return (request_line + headers + "\r\n\r\n" + self.body).encode()


    @classmethod
    def from_bytes(cls, binary_data: bytes):
        data = binary_data.decode().split('\r\n')
        method, url, _ = data[0].split()
        headers = {}
        for h in data[1:]:
            if ": " in h:
                key, value = h.split(": ", 1) 
                headers[key] = value

        return cls(method, url, headers, data[-1])


class HTTPResponse:
    def __init__(self, status_code: int, headers: dict, body: str):
        self.status_code = status_code
        self.headers = headers
        self.body = body

    def to_bytes(self) -> bytes:
        response_line = f'HTTP/1.1 {self.status_code} OK\r\n'
        headers = "".join(f'{k}: {v}\r\n' for k, v in self.headers.items())
        return (response_line + headers + '\r\n\r\n' + self.body).encode()

    @classmethod
    def from_bytes(cls, binary_data: bytes):
        data = binary_data.decode().split('\r\n')
        status_code = int(data[0].split()[1])
        headers = {}
        for h in data[1:]:
            if ": " in h:
                key, value = h.split(": ", 1) 
                headers[key] = value
                
        return cls(status_code, headers, data[-1])
