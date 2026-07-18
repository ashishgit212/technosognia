import socket
import sys

print("Checking port 3306...")
try:
    # Attempt to open a raw TCP connection to MySQL
    sock = socket.create_connection(('127.0.0.1', 3306), timeout=5)
    print("SUCCESS: Port 3306 is reachable!")
    sock.close()
except Exception as e:
    print(f"FAILED: Cannot reach port 3306. Error: {e}")
input("Press Enter to exit...")