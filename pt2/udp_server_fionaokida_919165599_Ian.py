import socket
import time

HOST = '127.0.0.1'
PORT = 5500

with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as server_socket:
    server_socket.bind((HOST, PORT))

    bytes_received = 0
    while True:
        if bytes_received == 0:
            tStart = time.time()
        
        data, addr = server_socket.recvfrom(1024)

        bytes_received += len(data) # increment by number of bytes received

        message = data.decode()
        if message == "DONE":
            tEnd = time.time()

            totTime = tEnd - tStart

            throughput = bytes_received / totTime
            kBps = throughput / 1024 # 1 kilobyte is 1024 bytes? 1000 bytes?

            response = f"Throughput is {kBps} kB/s"
            server_socket.sendto(response.encode(), addr)

            print(f"Total bytes: {bytes_received} bytes Total time: {totTime} seconds")
            bytes_received = 0
