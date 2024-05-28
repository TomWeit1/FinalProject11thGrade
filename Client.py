import socket

IP = 'localhost'
PORT = 12345


def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((IP, PORT))

    connected = True
    while connected:
        print(client.recv(5).decode())
        msg = "MOVE1"
        client.send(msg.encode())


if __name__ == '__main__':
    main()