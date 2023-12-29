import socket
import threading

HOST = "localhost"
PORT = 2024

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))


users = {}


def broadcast(message):
    """Sends message to all users in the chatroom."""
    for user in users:
        user.send(message)


def handle(user):
    """Handles user connection."""
    while True:
        username = users.get(user)
        message = user.recv(1024).decode()
        if message == "!quit\n":
            del users[user]
            user.close()
            broadcast(f"{username} left the chat\n".encode())
            print(f"{username} left the chat\n".encode())
            break
        broadcast(f"{username}: {message}".encode())


def recieve():
    """Sets up handling of incoming connetions."""
    while True:
        user, addr = server.accept()
        print(f"{str(addr)} connected!")

        user.send("Enter username: ".encode())
        username = user.recv(1024).decode().rstrip("\n")
        users[user] = username
        print(f"Username of the user is {username}")
        broadcast(f"{username} joined the chat room!\n".encode())
        user.send("Connected to the server\n".encode())
        thread = threading.Thread(target=handle, args=(user,))
        thread.start()


if __name__ == "__main__":
    server.listen(8)
    print("Server is listening...")

    recieve()
