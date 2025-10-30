import socket
import json

PROXY_HOST = "127.0.0.1"
PROXY_PORT = 5500  # Connect to proxy

jsoninfo = {
   "server_ip": "127.0.0.1",
   "server_port": 7000,
   "message": "ping",
}

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
   client_socket.connect((PROXY_HOST, PROXY_PORT))
   client_socket.sendall(json.dumps(jsoninfo).encode())
   data = client_socket.recv(1024)

print(f"Received {data.decode()!r} from {PROXY_HOST}:{PROXY_PORT}")

client_socket.close()
