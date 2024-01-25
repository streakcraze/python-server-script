"""script for running server.py as a linux daemon.
Run 'python daemon_server.py' to start the daemon.
It will generate a temporary 'daemon_server.pid' file
in the tmp folder containing a process ID value.
Run 'kill {the process ID value}' to stop the daemon."""

import os
from daemonize import Daemonize  # type: ignore
from server import start_server

if __name__ == "__main__":
    PID = "./tmp/daemon_server.pid"

    # Get the absolute path to the directory containing this script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    daemon = Daemonize(
        app="test_app", pid=PID, action=start_server, chdir=script_dir
    )

    daemon.start()
