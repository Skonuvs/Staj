import threading
import socket
import logging
from datetime import datetime

# Logging ayarları
logging.basicConfig(filename='logs/server.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

host = '0.0.0.0'
port = 65534

sv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sv.bind((host, port))
sv.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client):
    while True:
        try:
            message = client.recv(1024).decode('utf-8')
            broadcast(message.encode('utf-8'))
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = names[index]
            broadcast(f'{nickname} left the chat.'.encode('utf-8'))
            names.remove(nickname)
            logging.info(f'{nickname} left the chat.')
            break

def receive():
    while True:
        client, address = sv.accept()
        logging.info(f'Connected with {str(address)}')

        client.send('Name:'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        names.append(nickname)
        clients.append(client)

        logging.info(f"Name of the client is {nickname}.")
        broadcast(f"{nickname} connected to the chat.".encode('utf-8'))
        client.send('Connected to the chat.'.encode('utf-8'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()


logging.info("Server is listening...")
receive()
