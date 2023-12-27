import socket

HOST = "localhost"
PORT = 65432
with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"connected by: {addr}")
        while True:
            data = conn.recv(1024)
            if not data:
                break
            print(data)
            conn.sendall(data)
