import os
import sys
import time
import socket
from threading import Thread


IP = '127.0.0.1'
PORT = 9090
MAX_ClientConnections = 5
BUFFERSIZE = 1024


def msg_handling(conn, log_name):
    while True:
        data = conn.recv(BUFFERSIZE)
        if not data:
            continue
        if data.decode('utf-8') == 'exit':
            with open(log_name, 'a', encoding='utf-8') as f:
                f.write(f"{time.ctime()}: connection over, log out.\n")
            print("connection over, log out")
            break
        else:
            with open(log_name, 'a', encoding='utf-8') as f:
                f.write(data.decode('utf-8') + "\n")
            print("%s\n" % data.decode('utf-8'))
    conn.close()


class Client(Thread):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def run(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.connect((IP, PORT))
        files = os.listdir()
        log_name = self._name + "-client_log.txt"
        if log_name in files:
            print("Loading records...")
            with open(log_name, 'a', encoding='utf-8') as f:
                f.write(f"{time.ctime()}: connect to server.\n")
            with open(log_name, 'r', encoding='utf-8') as f:
                history = f.readlines()[-3:]
            for i in history:
                print(i)
        else:
            print("Initializing records...")
            with open(log_name, 'w', encoding='utf-8') as f:
                record = f"{time.ctime()}: chat records created by client-{self._name}\n."
                f.write(record)
            print(record)
        hello_msg = "Hello!+"+self._name
        client.send(hello_msg.encode('utf-8'))
        th_msg = Thread(target=msg_handling, args=(client, log_name))
        th_msg.start()
        try:
            while True:
                msg = input("\n> ")
                client.send(msg.encode('utf-8'))
        except:
            sys.exit(0)


if __name__ == "__main__":
    client1 = Client('Desline')
    # client2 = Client("April")

    client1.start()
    # client2.start()