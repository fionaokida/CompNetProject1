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
# import socket
# import json

# PROXY_HOST = "127.0.0.1"
# PROXY_PORT = 5500  # Client connects here

# # Define a simple IP blocklist. Add any blocked destination IPs here.
# BLOCKLIST = {
#    "10.0.0.1",
#    "192.0.2.1",
#    "203.0.113.5",
# }


# def handle_client(client_socket: socket.socket) -> None:
#    try:
#       data = client_socket.recv(4096)
#       if not data:
#          client_socket.sendall(b"Error")
#          return

#       try:
#          payload = json.loads(data.decode(errors="ignore"))
#       except json.JSONDecodeError:
#          client_socket.sendall(b"Error")
#          return

#       server_ip = payload.get("server_ip")
#       server_port = payload.get("server_port")
#       message = payload.get("message")

#       if not isinstance(server_ip, str) or not isinstance(server_port, int) or not isinstance(message, str):
#          client_socket.sendall(b"Error")
#          return

#       if server_ip in BLOCKLIST:
#          client_socket.sendall(b"Error")
#          return

#       with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as upstream:
#          upstream.settimeout(5)
#          try:
#             upstream.connect((server_ip, server_port))
#             upstream.sendall(message.encode())
#             response = upstream.recv(4096)
#          except OSError:
#             client_socket.sendall(b"Error")
#             return

#       client_socket.sendall(response if response else b"Error")
#    finally:
#       client_socket.close()


# def main() -> None:
#    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as proxy_socket:
#       proxy_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#       proxy_socket.bind((PROXY_HOST, PROXY_PORT))
#       proxy_socket.listen()
#       print(f"Proxy listening on {PROXY_HOST}:{PROXY_PORT}")
#       while True:
#          client_socket, _ = proxy_socket.accept()
#          # Simple sequential handling; acceptable for this assignment
#          handle_client(client_socket)


# if __name__ == "__main__":
#    main()


