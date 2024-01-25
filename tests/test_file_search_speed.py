"""speed test for file search option 6

Usage:
1. Adjust the 'SERVER' and 'PORT' variables to specify the server's 
   address and port.
2. Run the script using "pytest -s ./tests/test_algorithm_six_speed.py" 
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
def server_thread_fixture(request: pytest.FixtureRequest) -> Thread:
    """Fixture to run the server in a separate thread"""

    reread_on_query, linuxpath = request.param

    config = ConfigParser()
    config.read("config.ini")
    config.set("text_file", "reread_on_query", reread_on_query)
    config.set("text_file", "linuxpath", linuxpath)
    config.set("ssl", "ssl_auth", "False")

    with open("config.ini", "w", encoding="utf-8") as cfgfile:
        config.write(cfgfile)

    server = Thread(target=start_server)
    server.daemon = True
    server.start()
    # allow some time for the server to start
    time.sleep(1)

    return server


# 10k


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/10k.txt")], indirect=True
)
def test_string_found_reread_true_10k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[10k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/10k.txt")], indirect=True
)
def test_string_not_found_reread_true_10k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[10k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("False", "./text_files/10k.txt")], indirect=True
)
def test_string_found_reread_false_10k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[10k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/10k.txt")], indirect=True
)
def test_string_not_found_reread_false_10k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[10k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


# 100k


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/100k.txt")], indirect=True
)
def test_string_found_reread_true_100k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[100k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/100k.txt")], indirect=True
)
def test_string_not_found_reread_true_100k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[100k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("False", "./text_files/100k.txt")], indirect=True
)
def test_string_found_reread_false_100k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[100k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/100k.txt")], indirect=True
)
def test_string_not_found_reread_false_100k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[100k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


# 250k


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/250k.txt")], indirect=True
)
def test_string_found_reread_true_250k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[250k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/250k.txt")], indirect=True
)
def test_string_not_found_reread_true_250k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[250k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("False", "./text_files/250k.txt")], indirect=True
)
def test_string_found_reread_false_250k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[250k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/250k.txt")], indirect=True
)
def test_string_not_found_reread_false_250k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[250k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


# 500k


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/500k.txt")], indirect=True
)
def test_string_found_reread_true_500k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[500k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/500k.txt")], indirect=True
)
def test_string_not_found_reread_true_500k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[500k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("False", "./text_files/500k.txt")], indirect=True
)
def test_string_found_reread_false_500k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[500k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/500k.txt")], indirect=True
)
def test_string_not_found_reread_false_500k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[500k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


# 1000k


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/1000k.txt")], indirect=True
)
def test_string_found_reread_true_1000k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[1000k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/1000k.txt")], indirect=True
)
def test_string_not_found_reread_true_1000k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY TRUE] "
        f"[1000k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("False", "./text_files/1000k.txt")], indirect=True
)
def test_string_found_reread_false_1000k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;0;7;5;0;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING EXISTS\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[1000k LINES] [STRING EXISTS]: {end_time - start_time} seconds"
    )


@pytest.mark.parametrize(
    "server_thread", [("True", "./text_files/1000k.txt")], indirect=True
)
def test_string_not_found_reread_false_1000k(server_thread: Thread) -> None:
    """Test the server matching a string"""
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((SERVER, PORT))
    start_time = time.time()
    client.send("3;0;1;28;".encode("utf-8"))
    response = client.recv(1024).decode("utf-8")
    end_time = time.time()
    client.close()
    server_thread.join(timeout=2)

    assert response == "STRING NOT FOUND\n"

    # Calculate and print the time difference
    print(
        "[FILE SEARCH OPTION 6] [REREAD ON QUERY FALSE] "
        f"[1000k LINES] [STRING NOT FOUND]: {end_time - start_time} seconds"
    )
