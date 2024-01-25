"""testing server limitations in terms of number of
queries it can handle per second

Usage:
1. Adjust the 'SERVER' and 'PORT' variables to specify the server's 
   address and port.
2. Run the script using "pytest -s ./tests/test_query_rate.py" 
   to start the test.
   
Explanation:
query_rate=1 sends 1 query to the server in 1 second while
query_rate=2 sends 2 queries to the server in 1 second. However, after
query_rate=4 the client is unable to send the required number of queries.
For example, query_rate=5 may send 4 queries instead of 5 documenting
the limitations of the server."""

import socket
import time
from threading import Thread
from configparser import ConfigParser
import pytest
from ..server import start_server

SERVER = "127.0.1.1"
PORT = 5050
TEST_DURATION = 1


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


def test_query_rate_1(server_thread: Thread) -> None:
    """creates different clients sending 1 request
    per second to the server for the test_duration"""

    query_rate = 1

    print(f"Testing query rate: {query_rate} queries per second")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    i = 0
    start_time = time.time()
    while time.time() - start_time < TEST_DURATION:
        client.send("blah".encode("utf-8"))
        client.recv(1024).decode("utf-8")
        i += 1

        time.sleep(1 / query_rate)

    client.close()
    server_thread.join(timeout=2)

    assert i == query_rate * TEST_DURATION


def test_query_rate_2(server_thread: Thread) -> None:
    """creates different clients sending 2 requests
    per second to the server for the test_duration"""

    query_rate = 2

    print(f"Testing query rate: {query_rate} queries per second")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    i = 0
    start_time = time.time()
    while time.time() - start_time < TEST_DURATION:
        client.send("blah".encode("utf-8"))
        client.recv(1024).decode("utf-8")
        i += 1

        time.sleep(1 / query_rate)

    client.close()
    server_thread.join(timeout=2)

    assert i == query_rate * TEST_DURATION


def test_query_rate_3(server_thread: Thread) -> None:
    """creates different clients sending 3 requests
    per second to the server for the test_duration"""

    query_rate = 3

    print(f"Testing query rate: {query_rate} queries per second")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    i = 0
    start_time = time.time()
    while time.time() - start_time < TEST_DURATION:
        client.send("blah".encode("utf-8"))
        client.recv(1024).decode("utf-8")
        i += 1

        time.sleep(1 / query_rate)

    client.close()
    server_thread.join(timeout=2)

    assert i == query_rate * TEST_DURATION


def test_query_rate_4(server_thread: Thread) -> None:
    """creates different clients sending 4 requests
    per second to the server for the test_duration"""

    query_rate = 4

    print(f"Testing query rate: {query_rate} queries per second")

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))

    i = 0
    start_time = time.time()
    while time.time() - start_time < TEST_DURATION:
        client.send("blah".encode("utf-8"))
        client.recv(1024).decode("utf-8")
        i += 1

        time.sleep(1 / query_rate)

    client.close()
    server_thread.join(timeout=2)

    assert i == query_rate * TEST_DURATION
