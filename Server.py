import socket
from _thread import *
import threading

IP = 'localhost'
PORT = 12345


def client_handler(cli, addr):
    print(f"Client {cli} connected with addr: {addr}")

    connected = True
    while connected:
        pass


def main():
    client_threads = []
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server socket opened")

    srv_sock.bind((IP, PORT))
    print("Server socket binded")

    srv_sock.listen(5)

    while True:
        print("Waiting for connections")
        cli, addr = srv_sock.accept()
        thread = threading.Thread(target=client_handler, args=(cli, addr))
        thread.start()
        print(f"active connections: {threading.activeCount() - 1}")


if __name__ == '__main__':
    main()
