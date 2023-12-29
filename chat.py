import socket
import threading
import logging

HOST = "localhost"
PORT = 2024
TIMEOUT = 120
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%d-%b-%y %H:%M:%S",
)

users = {}


def broadcast(message):
    """Sends message to all users in the chatroom."""
    for user in users:
        user.send(message)


def handle(user):
    """Handles user connection."""
    user.settimeout(TIMEOUT)
    while True:
        username = users.get(user)
        try:
            message = user.recv(1024).decode()
        except socket.timeout:
            logging.warning(f"{username}'s connection timed out. Closing socket...")
            user.close()
            break

        if message == "!quit":
            del users[user]
            user.close()
            broadcast(f"{username} left the chat".encode())
            logging.info(f"{username} left the chat")
            break

        broadcast(f"{username}: {message}".encode())


def recieve():
    """Sets up handling of incoming connetions."""
    while True:
        user, addr = server.accept()
        logging.info(f"{str(addr)} connected!")
        user.send("username:".encode())
        username = user.recv(1024).decode().rstrip("\n")
        users[user] = username
        logging.info(f"Username: {username}")
        user.send("Connected to the server".encode())
        broadcast(f"{username} joined the chat room!".encode())
        thread = threading.Thread(target=handle, args=(user,))
        thread.start()


if __name__ == "__main__":
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(8)
    logging.debug("Server is listening...")
    try:
        recieve()
    except KeyboardInterrupt:
        logging.info("Stopping the server...")
    finally:
        server.close()
