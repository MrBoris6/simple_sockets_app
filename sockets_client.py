import socket
import threading

HOST = "localhost"
PORT = 2024


def recieve():
    """Handles recieving messages."""
    while True:
        try:
            message = client.recv(1024).decode()
            if message == "username:":
                client.send(username.encode())
            else:
                print(message)
        except Exception:
            print("An error occured!")
            client.close()
            break


def write():
    """Handles writing messages."""
    while True:
        message = f"{input('')}"
        client.send(message.encode())


if __name__ == "__main__":
    username = input("Choose a username: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT))
    threading.Thread(target=recieve).start()
    threading.Thread(target=write).start()
