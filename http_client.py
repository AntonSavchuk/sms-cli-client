import socket
import base64
import json
import toml 

from models import HTTPRequest, HTTPResponse

class HTTPClient:
    def __init__(self, conf_file: str = "config.toml"):
        try:
            self.config = toml.load(conf_file)
            self.host = "localhost"
            self.port = 4010
            self.username = self.config['server']['username']
            self.password = self.config['server']['password']
        except Exception as e:
            print('Configuration loading error: %s', e)
            exit(1)

    def send_sms(self, sender: str, recipient: str, message: str) -> HTTPResponse:
        try:
            auth = base64.b64encode(f'{self.username}:{self.password}'.encode()).decode()
            body = json.dumps({"sender": sender, "recipient": recipient, "message": message})

            body_bytes = body.encode("utf-8")
            headers = {
                "Authorization": f"Basic {auth}",
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Content-Length": str(len(body_bytes)),
            }

            request = HTTPRequest("POST", "/send_sms", headers, body).to_bytes()
            print("Sending request:")
            print(request.decode()) 

            print(f"Request body (length {len(body)}):")
            print(body)


            with socket.create_connection((self.host, self.port)) as sock:
                sock.sendall(request.split(b"\r\n\r\n")[0] + b"\r\n\r\n")
                sock.sendall(body_bytes) 
                sock.shutdown(socket.SHUT_WR) 
                response = sock.recv(4096)
            
            return HTTPResponse.from_bytes(response)
        except sock.timeout:
            print('Error: Server not responding (timeout)')
            exit(1)
        except socket.error as e:
            print('Connection error: %s', e)
            exit(1)
        except Exception as e:
            print('Unexpected error: %s', e)
            exit(1)