import socket
import json

HOST = "127.0.0.1"
PORT = 5500

BLOCKED_IPS = ["1.178.144.0", "104.239.128.16", "162.15.0.62"]

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
    proxy_socket.bind((HOST, PORT))
    proxy_socket.listen()
    print(f"Server listening on {HOST}:{PORT}")
    while True:
        client_socket, (client_addr, client_port) = proxy_socket.accept()
        data = client_socket.recv(1024)
        jsoninfo = json.loads(data.decode())

        server_ip = jsoninfo.get("server_ip")
        server_port = jsoninfo.get("server_port")
        message = jsoninfo.get("message")

        if server_ip in BLOCKED_IPS:
            client_socket.sendall(b"Error")
        else:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
                server_socket.connect((server_ip, server_port))
                server_socket.sendall(message.encode())
                response = server_socket.recv(1024)
                client_socket.sendall(response)

        client_socket.close()
