import socket
import base64
import json
import toml

from models import HTTPRequest, HTTPResponse

class HTTPClient:
    def __init__(self, conf_file: str = "config.toml"):
        pass

    def send_sms(self, sender: str, recipient: str, message: str) -> HTTPResponse:
        pass