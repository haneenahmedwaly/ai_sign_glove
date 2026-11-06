
import socket
import json

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

print("Waiting for Raspberry Pi Pico...")

while True:
    connection, address = server.accept()
    print("Connected by:", address)

    with connection:
        while True:
            data = connection.recv(1024)

            if not data:
                break

            try:
                readings = json.loads(data.decode("utf-8"))
                print("Received sensor readings:", readings)
            except json.JSONDecodeError:
                print("Invalid data received.")

    print("Pico disconnected.")
