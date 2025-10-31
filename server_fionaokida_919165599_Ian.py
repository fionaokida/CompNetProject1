import socket

HOST = "127.0.0.1"
PORT = 7000  

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
   server_socket.bind((HOST, PORT))
   server_socket.listen()
   print(f"Server listening on {HOST}:{PORT}") 
   while True:
       client_socket, (client_addr, client_port) = server_socket.accept()
       data = client_socket.recv(1024)
       if data == b"ping":
           print(f"Received {data.decode()!r} from {client_addr}:{client_port}") 
           client_socket.sendall(b"pong")

