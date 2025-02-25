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
        try:
            data = binary_data.decode(errors="ignore").split("\r\n")

            if not data or len(data[0].split()) < 2:
                return cls(500, {}, "Invalid response")  # Возвращаем 500, если статус не найден

            status_code = int(data[0].split()[1])

            headers = {}
            body_index = 1
            for i, h in enumerate(data[1:], start=1):
                if h == "":  # Пустая строка отделяет заголовки от тела
                    body_index = i + 1
                    break
                if ": " in h:
                    key, value = h.split(": ", 1)
                    headers[key] = value

            body = "\n".join(data[body_index:]) if body_index < len(data) else ""

            return cls(status_code, headers, body)

        except Exception as e:
            print(f"Ошибка парсинга ответа: {e}")
            return cls(500, {}, "Invalid response")



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
        try:
            data = binary_data.decode(errors="ignore").split("\r\n")

            if not data or len(data[0].split()) < 2:
                return cls(500, {}, "Invalid response") 

            status_code = int(data[0].split()[1])

            headers = {}
            body_index = 1
            for i, h in enumerate(data[1:], start=1):
                if h == "": 
                    body_index = i + 1
                    break
                if ": " in h:
                    key, value = h.split(": ", 1)
                    headers[key] = value

            body = "\n".join(data[body_index:]) if body_index < len(data) else ""

            return cls(status_code, headers, body)

        except Exception as e:
            print(f"Ошибка парсинга ответа: {e}")
            return cls(500, {}, "Invalid response")


