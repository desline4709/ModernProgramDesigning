import socket
from threading import Thread, Lock
import os
import re
import time


IP = '127.0.0.1'
PORT = 9090
MAX_ClientConnections = 5
BUFFERSIZE = 1024
Lock = Lock()
client_conns = []


def handle_client(conn, name, log_name, client_conns):
    print(f"Welcome client {name} !")
    if client_conns:
        for client in client_conns:
            client[0].send(f"Welcome client {name} !".encode("utf-8"))
    while 1:
        try:
            msg = conn.recv(BUFFERSIZE)
            msg = msg.decode('utf-8')  # 先解码
            if msg == 'exit':
                conn.send("exit".encode('utf-8'))  # 给客户端发送退出指令
                with Lock:
                    with open(log_name, 'a', encoding='utf-8') as f:
                        f.write(f"{time.ctime()}: {name} leave the chatroom...\n")
                print("{} leave the chatroom...".format(name))
                if client_conns:
                    for client in client_conns:
                        client[0].send(f"{name} leave the chatroom...".encode("utf-8"))
                break
            else:
                msg = f"{time.ctime()}: " + f"{name}: " + msg + "\n"
                with Lock:
                    with open(log_name, 'a', encoding='utf-8') as f:
                        f.write(msg)
                if "@" in msg:
                    # 信息中可能要@某人
                    message = msg[msg.index("@"):]
                    if " " in message:
                        prefix = message[:message.index(' ')]  # 截取第一个空格前的部分，即"@xxx"
                    else:
                        prefix = message
                    # print(f"{prefix}")
                    dest_name = re.search("@.+", prefix).group(0)[1:]  # 截取@后的内容
                    flag = 0
                    for client in client_conns:
                        if dest_name == client[1]:
                            client[0].send(msg.encode('utf-8'))  # 找出被@的人，并把信息发给他
                            flag = 1
                            break
                    if flag == 0:
                        # 此时表示@不是用来私有转发的字符，信息发给所有人
                        for client in client_conns:
                            client[0].send(msg.encode('utf-8'))
                else:
                    # 不带@的正常信息，发给所有人
                    for client in client_conns:
                        client[0].send(msg.encode('utf-8'))

            print("{}:{}".format(name, msg))
            with Lock:
                with open(log_name, 'a', encoding='utf-8') as f:
                    f.write("{}: ".format(time.ctime()) + "{}:{}\n".format(name, msg))
        except Exception as e:
            print("server error %s" % e)
            with Lock:
                with open(log_name, 'a', encoding='utf-8') as f:
                    f.write(f"{time.ctime()}: server error {e}!\n")
            break
    client_conns.remove((conn, f"{name}"))
    conn.close()


class Manager(Thread):
    def __init__(self, name):
        super().__init__()
        self._name = name

    def run(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # 端口释放后马上可以被重新使用
        server.bind((IP, PORT))
        server.listen(MAX_ClientConnections)

        files = os.listdir()
        log_name = self._name + "_ChatRecords.txt"
        if log_name in files:
            print("Loading records ...\n")
            with open(log_name, 'a', encoding='utf-8') as f:
                record = f"{time.ctime()}: loading records by server-{self._name}."
        else:
            print("Initializing records...\n")
            with open(log_name, 'w', encoding='utf-8') as f:
                record = f"{time.ctime()}: chat records created by server-{self._name}.\n"
                f.write(record)
            print(record)

        print("Chatroom server online ...\n")
        print("Welcome to chat here!")
        while 1:
            conn, addr = server.accept()  # 这里会阻塞直到接收到客户端连接
            client_hello = conn.recv(BUFFERSIZE)
            client_name = client_hello.decode('utf-8').split('+')[1]
            client_msg = client_hello.decode('utf-8').split("+")[0]
            print(f"client {client_name} says {client_msg}")
            client_conns.append((conn, client_name))
            t = Thread(target=handle_client, args=(conn, client_name, log_name, client_conns))
            t.start()
        server.close()


if __name__ == "__main__":
    server = Manager("Chatroom-Heaven")
    server.start()
    server.join()