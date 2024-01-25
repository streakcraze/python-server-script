# Python Sockets Project

This is a simple Python project that demonstrates socket communication between a server and a client. It includes a server implementation (`server.py`), a daemonized server (`daemon_server.py`), and a client (`client.py`).

## Installation

1. Navigate to the project directory:

   ```bash
   cd your-sockets-project
   ```

2. Create and activate a virtual environment:

   ```bash
   python -m venv venv
   source venv/bin/activate
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Running the Server

#### Basic Server

In server.py, adjust the SERVER and PORT literals as needed:

```bash
# Update these values accordingly
SERVER = "localhost"
PORT = 8080
```

Run the basic server:

```bash
python server.py
```

#### Daemonized Server

Run the daemonized server:

```bash
python daemon_server.py
```

It will generate a temporary 'daemon_server.pid' file in the tmp folder containing a process ID value. Run the following command to stop the daemon:

```bash
kill $(cat tmp/daemon_server.pid)
```

## Configuration
The project includes a configuration file (config.ini) with the following settings:

[text_file] Section:
- linuxpath: The path to the text file used for searching string sent by client.
- reread_on_query: Whether to reread the file on each client query (True/False).

[ssl] Section:
- ssl_auth: Whether SSL authentication is enabled (True/False).
- certfile: The path to the SSL certificate file.
- keyfile: The path to the SSL key file.

### Running the Client

In client.py, adjust the SERVER and PORT literals as needed:

```bash
# Update these values accordingly
SERVER = "localhost"
PORT = 8080
```

Run the client:

```bash
python client.py
```

## Testing
This project uses pytest for testing.
In test files contained in tests folder, adjust the SERVER and PORT literals as needed:

```bash
# Update these values accordingly
SERVER = "localhost"
PORT = 8080
```

Run the tests with the following command:

```bash
pytest
```

Run specific test files using:

```bash
pytest ./tests/{name of test file}
```

For the file search speed tests it is useful to add the -s flag:

```bash
pytest -s ./tests/{name of test file}
```

## Type Checking

Type checking is performed using mypy. Run mypy with the following command:

```bash
mypy {name of file}
```

## Additional Information

### Third-party Libraries

- pytest: Testing framework.
- mypy: Static type checker for Python.
- daemonize: Library for daemonizing processes.

## Contributing

Feel free to contribute to this project by opening issues or submitting pull requests.

## License

This project is licensed under the [MIT License](LICENSE).
