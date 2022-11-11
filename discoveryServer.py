import time
import socket
import threading

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONN_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set() # To keep track of all the clients connected
users = dict() # To associate each address to username


def newNode():
    server.listen() # Start listening on the address ADDR
    addrMsg = "\n[NODES CONNECTED]"
    while True:
        node, addr = server.accept()
        username = node.recv(1024).decode(FORMAT)
        users[addr] = username
        addrMsg += "\n" + username
        print(f"[NEW CONNECTION] {addr}: {username}")
        time.sleep(0.5) # Waiting so that the connected node can receive the message as well
        clients.add(node)
        for c in clients:
            c.sendall(str(addrMsg).encode(FORMAT))
        thread = threading.Thread(target=nodeDisconnection, args=(node, addr))
        thread.start()
        

def nodeDisconnection(node, addr):
    while True:
        msg = node.recv(1024).decode(FORMAT)
        print(msg)
        if msg == DISCONN_MESSAGE:
            print(f"[DISCONNECTION] {addr}")
            clients.remove(node)
            addrMsg = users.pop(addr) + " disconnected" 
            for c in clients: # Notifying the nodes on the disconnection
                c.sendall(str(addrMsg).encode(FORMAT))
            break
        else:
            continue

def start():
    print("[DISCOVERY SERVER STARTED]")
    thread = threading.Thread(target=newNode)
    thread.start()


start()