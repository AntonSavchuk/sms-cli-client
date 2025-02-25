import pytest
import json
import socket
import argparse
from unittest.mock import patch, MagicMock

from models import HTTPRequest, HTTPResponse
from http_client import HTTPClient
from cli import send_sms

# ==== Тесты для HTTPRequest ====

def test_http_request_to_bytes():
    request = HTTPRequest(
        "POST",
        "/send_sms",
        {"Content-Type": "application/json"},
        '{"sender": "123", "recipient": "456", "message": "Hello"}'
    )
    request_bytes = request.to_bytes()
    assert isinstance(request_bytes, bytes)
    assert b"POST /send_sms HTTP/1.1" in request_bytes
    assert b"Content-Type: application/json" in request_bytes

def test_http_request_from_bytes():
    response_bytes = (
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
        b'{"status": "success", "message_id": "123456"}'
    )
    response = HTTPResponse.from_bytes(response_bytes)
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/json"
    assert json.loads(response.body) == {"status": "success", "message_id": "123456"}

# ==== Тесты для HTTPResponse ====

def test_http_response_to_bytes():
    response = HTTPResponse(200, {"Content-Type": "application/json"}, '{"status": "success"}')
    response_bytes = response.to_bytes()
    assert isinstance(response_bytes, bytes)
    assert b"HTTP/1.1 200 OK" in response_bytes
    assert b"Content-Type: application/json" in response_bytes
    assert b'{"status": "success"}' in response_bytes

def test_http_response_from_invalid_bytes():
    response_bytes = b"Invalid Response"
    response = HTTPResponse.from_bytes(response_bytes)
    assert response.status_code == 500
    assert response.body == "Invalid response"

# ==== Тесты для HTTPClient ====

@pytest.fixture
def http_client():
    with patch("toml.load", return_value={"server": {"username": "user", "password": "pass"}}):
        return HTTPClient()

def test_http_client_init(http_client):
    assert http_client.username == "user"
    assert http_client.password == "pass"

@patch("socket.create_connection")
def test_http_client_send_sms(mock_socket, http_client):
    mock_sock = MagicMock()
    mock_socket.return_value.__enter__.return_value = mock_sock
    response_data = (
        b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n"
        b'{"status": "success", "message_id": "123"}'
    )
    mock_sock.recv.return_value = response_data

    response = http_client.send_sms("123", "456", "Hello")
    assert response.status_code == 200
    assert json.loads(response.body) == {"status": "success", "message_id": "123"}

@patch("socket.create_connection", side_effect=socket.timeout)
def test_http_client_timeout(mock_socket, http_client):
    with pytest.raises(RuntimeError, match="Ошибка при выполнении запроса"):
        http_client.send_sms("123", "456", "Hello")

@patch("socket.create_connection", side_effect=socket.error)
def test_http_client_connection_error(mock_socket, http_client):
    with pytest.raises(RuntimeError, match="Ошибка при выполнении запроса"):
        http_client.send_sms("123", "456", "Hello")

# ==== Тесты для CLI ====

@patch("http_client.HTTPClient.send_sms")
def test_cli_send_sms(mock_send_sms, capsys):
    mock_send_sms.return_value = HTTPResponse(200, {}, '{"status": "success"}')

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')
    send_parser = subparsers.add_parser("send")
    send_parser.add_argument("sender")
    send_parser.add_argument("recipient")
    send_parser.add_argument("message")
    send_parser.set_defaults(func=send_sms)

    args = parser.parse_args(["send", "123", "456", "Hello"])
    args.func(args)

    captured = capsys.readouterr()
    assert "Server response:  200 {\"status\": \"success\"}" in captured.out
