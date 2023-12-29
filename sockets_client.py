import socket
import threading

HOST = "localhost"
PORT = 2024


def receive():
    """Handles receiving messages."""
    while True:
        try:
            message = client.recv(1024).decode()
            if not message:
                break
            if message == "username:":
                client.send(username.encode())
            else:
                print(message)
        except Exception as e:
            print(f"An error occurred!: {e}")
            break


def write():
    """Handles sending messages."""
    while True:
        try:
            message = f"{input('')}"
            client.send(message.encode())
            if message == "!quit":
                break
        except Exception as e:
            print(f"An error occurred: {e}")
            break


if __name__ == "__main__":
    try:
        username = input("Choose a username: ")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((HOST, PORT))

        thread_receive = threading.Thread(target=receive)
        thread_write = threading.Thread(target=write)

        thread_receive.start()
        thread_write.start()
        thread_receive.join()
        thread_write.join()
    except KeyboardInterrupt:
        ...
    finally:
        print("Exiting chatroom...")
        client.send("!quit".encode())
        client.close()
