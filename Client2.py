import socket

IP = 'localhost'
PORT = 12345


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    connected = True
    while connected:
        print(client.recv(5).decode())


if __name__ == '__main__':
    main()