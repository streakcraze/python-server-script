"""This script implements a simple server using Python's socket module. 
It creates a server socket, binds it to a specified address and port, 
and listens for incoming client connections. For each incoming connection, 
a new thread is spawned to handle the client communication.

Dependencies:
socket: low-level networking functionality for creating and managing sockets.
threading: concurrent execution of code by creating and managing threads.
configparser: reading configuration files and access their content.
time: working with time values, measuring time intervals, and formatting time.
logging: emitting customizable log messages to console, files, etc.
ssl: secure communication through encryption and authentication.
errno: provides symbolic error codes for exception handling.

Usage:
1. Adjust the 'SERVER' and 'PORT' variables to specify the server's 
   address and port.
2. Run the script using "python server.py" to start listening for incoming 
   connections.
3. Clients can then connect to the server's address and port."""

import socket
import threading
from configparser import ConfigParser
import time
import logging
import ssl
import errno

SERVER = "127.0.1.1"
PORT = 5050
ADDR = (SERVER, PORT)
FORMAT = "utf-8"


def handle_client(conn: socket.socket, addr: tuple[str, int]) -> None:
    """function processing client data in different threads concurrently"""

    logging.debug("[NEW CONNECTION] %s connected", addr)

    # reading values from config file
    config = ConfigParser()
    config.read("config.ini")
    text_file_path = config.get("text_file", "linuxpath")
    reread_on_query = config.getboolean("text_file", "reread_on_query")

    # file read for REREAD_ON_QUERY=False
    with open(text_file_path, "r", encoding=FORMAT) as f:
        # appends newline character at start and end of
        # file string
        file_lines = "\n" + f.read() + "\n"

    try:
        while True:
            # blocking line of code waiting for message from client
            msg = conn.recv(1024).decode(FORMAT)

            # break the connection if no message is sent
            if not msg:
                break

            # record the start of execution time
            start_time = time.time()

            # file read for REREAD_ON_QUERY=True
            if reread_on_query:
                with open(text_file_path, "r", encoding=FORMAT) as f:
                    # appends newline character at start and end of
                    # file string
                    file_lines = "\n" + f.read() + "\n"

            msg = "\n" + msg + "\n"
            # Check if the modified message is in the file content
            if msg in file_lines:
                search_result = "STRING EXISTS\n"
            else:
                search_result = "STRING NOT FOUND\n"

            conn.send(search_result.encode(FORMAT))

            # record the stop of execution time
            elapsed_time = time.time() - start_time
            # log info to console and log file for debug
            logging.debug(
                "[QUERY] requesting_address: %s, query_string: %s, "
                "query_result: %s, execution_time: %ss",
                addr,
                msg.strip("\n"),
                search_result.rstrip("\n"),
                elapsed_time,
            )
    except ConnectionResetError as e:
        print(f"ConnectionResetError: {e}")
    finally:
        # closing the client connection
        logging.debug("[CLOSED CONNECTION] %s disconnected", addr)
        conn.close()


def start_server() -> None:
    """function starting up server socket to listen, accept, and
    create different threads for client connections"""

    # configuring log output format
    logging.basicConfig(
        format="%(levelname)s::%(asctime)s::%(message)s",
        level=logging.DEBUG,
        datefmt="%m/%d/%Y %I:%M:%S%p",
        handlers=[
            logging.FileHandler("./tmp/server.log"),
            logging.StreamHandler(),
        ],
    )

    # reading values from config file
    config = ConfigParser()
    config.read("config.ini")
    ssl_configured = config.getboolean("ssl", "ssl_auth")
    sslcert_file_path = config.get("ssl", "certfile")
    sslkey_file_path = config.get("ssl", "keyfile")

    try:
        # creating the server socket
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        logging.debug("[STARTING] server is starting ...")
        # binding the server socket to a specific address and port
        server.bind(ADDR)
        # listen for incoming connections on the server socket
        server.listen()
        logging.debug("[LISTENING] server is listening on %s:%s", SERVER, PORT)

        while True:
            # conn is a standard python socket, addr is where it originated
            client_conn, addr = server.accept()
            # ssl authentication is configurable (can be turned on/off)
            if ssl_configured:
                # creating SSLContext with default settings
                context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
                # loading CA and corresponding private key
                context.load_cert_chain(
                    certfile=sslcert_file_path, keyfile=sslkey_file_path
                )
                # wrap the standard socket with the SSLContext,
                # now it is a secure connection
                secure_client_conn = context.wrap_socket(
                    client_conn, server_side=True
                )
                # using secure socket for handling client connection
                thread = threading.Thread(
                    target=handle_client, args=(secure_client_conn, addr)
                )
            else:
                # using standard socket if ssl is turned off
                thread = threading.Thread(
                    target=handle_client, args=(client_conn, addr)
                )

            thread.start()
            logging.debug(
                "[ACTIVE CONNECTIONS] %s", threading.active_count() - 1
            )
            thread.join(timeout=2)
    except KeyboardInterrupt:
        # handle CTRL+C input from the user for program termination
        print("[KEYBOARD INTERRUPT] closing the server ...")
    except socket.error as e:
        # handle specified address already being in use
        if e.errno == errno.EADDRINUSE:
            print("[ERROR] address already in use, choose a different port")
        else:
            print(f"Socket error: {e}")
    finally:
        # closing the server socket
        server.close()
        logging.debug("[CLOSED] server is closed")


if __name__ == "__main__":
    start_server()
