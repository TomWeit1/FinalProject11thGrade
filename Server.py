import socket
from _thread import *
import threading

IP = 'localhost'
PORT = 12345


def client_handler(cli1, addr1, cli2, addr2):
    print(f"Client {cli1} connected with addr: {addr1}")
    print(f"Client {cli2} connected with addr: {addr2}")

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
        print("Waiting for connection 1\n")
        cli1, addr1 = srv_sock.accept()
        print("Waiting for connection 2\n")
        cli2, addr2 = srv_sock.accept()

        thread = threading.Thread(target=client_handler, args=(cli1, addr1, cli2, addr2))
        thread.start()
        #print(f"active connections: {threading.activecount() - 1}")


if __name__ == '__main__':
    main()
