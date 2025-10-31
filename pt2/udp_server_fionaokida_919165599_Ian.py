import socket

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 5500

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as client_socket:

    bytes_left = 100 * 1024 * 1024  # 100 MB
    packet = b'.' * 1024 # packets are 1 KB

    while bytes_left > 0:
        client_socket.sendto(packet, (SERVER_HOST, SERVER_PORT))
        bytes_left -= len(packet)

    client_socket.sendto(b"DONE", (SERVER_HOST, SERVER_PORT))

    response, _ = client_socket.recvfrom(1024)

    kBps = response.decode()
    print(f"{kBps}")

    client_socket.close()
