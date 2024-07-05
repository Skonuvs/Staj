import socket
import threading
import os
import time

name = os.getenv("USERNAME", "DefaultUser")
if not name:
    raise ValueError("USERNAME environment variable not set")

cl = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

while True:
    try:
        cl.connect(('niyazi', 65534))
        break
    except ConnectionRefusedError:
        print("Server henüz başlatılmadı, 5 saniye sonra tekrar denenecek...")
        time.sleep(5)

def receive():
    while True:
        try:
            message = cl.recv(1024).decode('utf-8')
            if message == 'Name:':
                cl.send(name.encode('utf-8'))
            else:
                print(message)
        except:
            print("An error occurred")
            cl.close()
            break

def write():
    while True:
        message = f'{name}: giriş yaptı'
        cl.send(message.encode('utf-8'))
        time.sleep(5)

rc_th = threading.Thread(target=receive)
rc_th.start()

wr_th = threading.Thread(target=write)
wr_th.start()
