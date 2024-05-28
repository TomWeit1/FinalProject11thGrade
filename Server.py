import socket
from _thread import *
import threading

IP = 'localhost'
PORT = 12345


def start_game(cli1, cli2):
    msg = "STRT"
    cli1.send((msg + "1").encode())
    cli2.send((msg + "2").encode())


def handle_msg(data, cli, id):
    msg = ""
    if data == "MOVE":
        move = cli.recv(2).decode()
        msg = "MOVE" + str(id) + move
    if data == "SHOT":
        msg = "SHOT" + str(id) + "00"  # 00 is a filler to make this message length be 6
    if data == "OVER":
        loser_id = cli.recv(1).decode()
        msg = "OVER" + loser_id
    if data == "EXIT":
       pass

    print(msg)
    return msg


def send_both(msg, cli1, cli2):
    cli1.send(msg.encode())
    cli2.send(msg.encode())


def handle(cli, id, other_cli):
    while True:
        try:
            data = cli.recv(4).decode()
            msg = handle_msg(data, cli, id)
            send_both(msg, cli, other_cli)

        except socket.error as err:
            print(f'Socket Error exit client loop: err:  {err}')
            break
        except Exception as  err:
            print(f'General Error %s exit client loop: {err}')
            print(traceback.format_exc())
            break


def client_handler(cli1, addr1, cli2, addr2):
    print(f"Client {cli1} connected with addr: {addr1}")
    print(f"Client {cli2} connected with addr: {addr2}")

    connected = False

    try:
        start_game(cli1, cli2)
        connected = True
    except Exception as err:
        print(err)

    if connected:
        thread1 = threading.Thread(target=handle, args=(cli1, 1, cli2))
        thread1.start()
        thread2 = threading.Thread(target=handle, args=(cli2, 2, cli1))
        thread2.start()


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
        # print(f"active connections: {threading.activecount() - 1}")


if __name__ == '__main__':
    main()
