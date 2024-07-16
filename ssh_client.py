import socket

# TCP sunucu bilgileri
TCP_HOST = "127.0.0.1"
TCP_PORT = 53947

def start_client():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((TCP_HOST, TCP_PORT))
    print(f"Connected to TCP server at {TCP_HOST}:{TCP_PORT}")

    while True:
        command = input("Enter command to execute on SSH server: ")
        if command.lower() == "exit":
            break

        # Komutu sunucuya gönder
        client.send(command.encode())

        # Sunucudan sonucu al
        response = client.recv(4096).decode()  # Bu değeri 4096 olarak arttırdık
        print(f"Response:\n{response}")

    client.close()

if __name__ == "__main__":
    start_client()
