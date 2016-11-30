# !/usr/bin/env python
import socket
import json

TCP_IP              = '127.0.0.1'
SCREEN_PORT         = 5006
BUFFER_SIZE         = 1024

def get_text(PORT):
    # RECEIVE MESSAGE FROM SOCKET
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    s.bind((TCP_IP, PORT))
    s.listen(1)
    conn, addr = s.accept()

    data = conn.recv(BUFFER_SIZE)
    print("RECEIVED: "+data.decode("utf-8"))

    return data.decode("utf-8")


def main():
    while 1:
        recv = get_text(SCREEN_PORT)
        print("TEXT RECEIVED: "+str(recv))

if __name__ == "__main__":
    main()