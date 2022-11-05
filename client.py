import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

def connect():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR) # We're connecting to an existing socket, not binding a new one
    
    return client

def send(client, msg):
    message = msg.encode(FORMAT)
    client.send(message)


client = connect()
msg = input("Inserisci messaggio: ")
send(client, msg)
input()
send(client, DISCONNECT_MESSAGE)