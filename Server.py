import socket
from _thread import *
import threading

if __name__ == '__main__':
    client_threads = []
    srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("Server socket opened")

    srv_sock.bind(('localhost', 12345))
    print("Server socket binded")

    srv_sock.listen(5)