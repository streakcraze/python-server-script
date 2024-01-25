"""client script for establishing connection and exchanging messages
with server. also configures ssl communication.

Usage:
1. Adjust the 'SERVER' and 'PORT' variables to specify the server's 
   address and port.
2. Run the script using 'python client.py' to start the test."""

import socket
from configparser import ConfigParser
import ssl

PORT = 5050
SERVER = "127.0.1.1"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"

config = ConfigParser()
config.read("config.ini")
ssl_configured = config.getboolean("ssl", "ssl_auth")
sslcert_file_path = config.get("ssl", "certfile")


def start_client() -> None:
    """function creating a client socket, establishing a connection
    with the server, sending string input from user to server, and
    printing server response to the string match"""

    try:
        print("[STARTING] establishing a new connection ...")

        if ssl_configured:
            context = ssl.create_default_context()
            context.load_verify_locations(sslcert_file_path)
            client = context.wrap_socket(
                socket.socket(socket.AF_INET, socket.SOCK_STREAM),
                server_hostname="ARNOLD",
            )
        else:
            client = socket.socket(
                socket.AF_INET, socket.SOCK_STREAM
            )  # type: ignore

        client.connect(ADDR)
        print("[SUCCESS] connection established")

        while True:
            client_input = input("Enter search string [^C to exit]: ")
            if len(client_input) > 0:
                message = client_input.encode(FORMAT)
                client.send(message)
                res = client.recv(1024).decode(FORMAT)
                print(f"[RESPONSE] {res}")
    except KeyboardInterrupt:
        print("\n[KEYBOARD INTERRUPT] closing the connection ...")
    except ConnectionRefusedError:
        print("\n[CONNECTION ERROR] server may not be running ...")
    finally:
        # Close the server socket in the finally block
        client.close()
        print("[CLOSED] connection terminated")


if __name__ == "__main__":
    start_client()
