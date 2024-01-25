"""tests for correct workflow and edge cases

Usage:
1. Adjust the 'SERVER' and 'PORT' variables to specify the server's 
   address and port.
2. Run the script using "pytest -s ./tests/test_server_workflow.py" 
   to start the test."""

import socket
import time
from threading import Thread
from configparser import ConfigParser
import pytest
from ..server import start_server

SERVER = "127.0.1.1"
PORT = 5050


@pytest.fixture(name="server_thread")
def server_thread_fixture() -> Thread:
    """fixture to run the server in a separate thread"""

    config = ConfigParser()
    config.read("config.ini")
    config.set("text_file", "linuxpath", "./text_files/250k.txt")
    config.set("ssl", "ssl_auth", "False")
    with open("config.ini", "w", encoding="utf-8") as cfgfile:
        config.write(cfgfile)

    server = Thread(target=start_server)
    server.daemon = True
    server.start()
    # Allow some time for the server to start
    time.sleep(2)
    # Provide the server thread to the test
    return server


def test_string_found_response(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"


def test_string_not_found_response(server_thread: Thread) -> None:
    """Test the server not matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    client.send("3;0;1;28;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"


def test_multiple_connections(server_thread: Thread) -> None:
    """Test the server's ability to handle multiple connections"""
    client_sockets = []
    messages = ["3;0;1;28;0;7;5;0;", "3;0;1;28;0;", "blah"]
    expected_responses = [
        "STRING EXISTS\n",
        "STRING NOT FOUND\n",
        "STRING NOT FOUND\n",
    ]

    for message in messages:
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client_sockets.append(client)
        client.send(message.encode("utf-8"))

    # responses from the server
    received_data = [
        client.recv(1024).decode("utf-8") for client in client_sockets
    ]

    for client in client_sockets:
        client.close()

    server_thread.join(timeout=2)

    assert received_data == expected_responses


def test_long_message(server_thread: Thread) -> None:
    """Test the server's ability to handle long messages"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    # Create a long message
    long_message = b"A" * 1024 * 1024  # 1MB message

    client.send(long_message)
    response = client.recv(1024).decode("utf-8")
    client.close()
    server_thread.join(timeout=2)

    assert response.find("STRING NOT FOUND\n") != -1
