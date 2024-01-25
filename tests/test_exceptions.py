"""tests for exceptions raised

Usage:
1. Adjust the 'SERVER' and 'PORT' variables to specify the server's 
   address and port.
2. Run the script using "pytest -s ./tests/test_exceptions.py" 
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


def test_connection_refused_exception(server_thread: Thread) -> None:
    """test if the server gracefully handles connection failures"""

    with pytest.raises(ConnectionRefusedError):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Assuming the server is not running on this adddress
        client.connect((SERVER, 8080))
        client.close()
        server_thread.join(timeout=2)


def test_invalid_host_exception(server_thread: Thread) -> None:
    """test if the server gracefully handles connections to invalid hosts"""

    with pytest.raises(socket.gaierror):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Trying to connect to an invalid host
        client.connect(("invalidhost", 80))
        client.close()
        server_thread.join(timeout=2)


def test_socket_error_exception(server_thread: Thread) -> None:
    """test if the server gracefully handles socket errors"""

    with pytest.raises(socket.error):
        # Cause a socket error (e.g., by providing an invalid address family)
        client = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)
        client.connect((SERVER, PORT))
        client.close()
        server_thread.join(timeout=2)
