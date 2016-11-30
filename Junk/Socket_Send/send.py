# !/usr/bin/env python
import socket
import json
import time

TCP_IP = '127.0.0.1'
IMAGE_PORT = 5005
BUFFER_SIZE = 1024
MESG = '{"change_database":"1","object":{"template_file": "TEMPLATE_TEST.jpg","screen_file":"SCREEN_TEST.jpg"}}'
MESG2 = '{"change_database":"0","object":[{"sign_number":"1","distance":".67"},{"sign_number":"2","distance":".67"},{"sign_number":"3","distance":".20"},{"sign_number":"4","distance":".67"}]}'


def send_marker(MARKER):

    json.dumps()
    send_text(MARKER)

def init_send_conn(PORT):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((TCP_IP, IMAGE_PORT))
    print("SOCKET "+str(IMAGE_PORT)+" INITIALIZED.")
    return s

def send_text(MESSAGE, PORT):
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect((TCP_IP, PORT))
    print("Sending: "+MESSAGE)
    s.send(bytes(MESSAGE,'utf-8'))
    s.close()

def main():
    t = 1
    #send_text('{"window": {"title": "Sample Konfabulator Widget","name": "main_window","width": 500,"height": 500}}', TCP_PORT)
    for x in range(0, 15):
        if x==14:
            send_text(t, IMAGE_PORT)
            x = 0
        time.sleep(1)
            

if __name__ == "__main__":
    main()
