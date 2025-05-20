import os
import sys
import subprocess
import webbrowser
import time


def main():
    """Start the Flask web application and open it in a browser."""
    server_script = os.path.join('webapp', 'server.py')
    process = subprocess.Popen([sys.executable, server_script])
    try:
        # Give the server a moment to start
        time.sleep(1)
        webbrowser.open('http://localhost:5000')
        process.wait()
    except KeyboardInterrupt:
        pass
    finally:
        process.terminate()


if __name__ == '__main__':
    main()
