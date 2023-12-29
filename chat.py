import socket
import threading
import logging

HOST = "localhost"
PORT = 2024
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

    while True:
        try:
            username = users.get(user)
            message = user.recv(1024).decode()
            if message == "!quit":
                del users[user]
                user.close()
                broadcast(f"{username} left the chat".encode())
                logging.info(f"{username} left the chat")
                break

            broadcast(f"{username}: {message}".encode())
        except Exception as e:
            logging.warning(f"An eror occured for {username}: {e}.")
            logging.info("Closing the socket...")
            del users[user]
            user.close()
            break


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
        pass
    except Exception as e:
        logging.warning(f"An error occured: {e}")
    finally:
        logging.info("Stopping the server...")
        server.close()
