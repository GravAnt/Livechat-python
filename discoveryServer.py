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
sockets = dict() # To associate each address to socket
users = dict() # To associate each address to username


def newNode():
    server.listen() # Start listening on the address ADDR
    while True:
        node, addr = server.accept()
        username = node.recv(1024).decode(FORMAT)
        users[addr] = username
        sockets[addr] = node
        nodesConnected = "\n[NODES CONNECTED]"
        for clientAddr, clientUsername in users.items():
            nodesConnected += "\n" + clientUsername
        print(f"[NEW CONNECTION] {addr}: {username}")
        time.sleep(0.5) # Waiting so that the connected node can receive the message as well
        clients.add(node)
        for c in clients:
            c.sendall(nodesConnected.encode(FORMAT))
        thread = threading.Thread(target=nodeHandling, args=(node, addr, username))
        thread.start()
        

def nodeHandling(node, addr, username):
    while True:
        msg = node.recv(1024).decode(FORMAT)
        if msg == DISCONN_MESSAGE:
            print(f"[DISCONNECTION] {addr}: {username}")
            clients.remove(node)
            sockets.pop(addr)
            clientDisconnection = "[NEW DISCONNECTION] " + users.pop(addr)
            node.close()
            for c in clients: # Notifying the nodes on the disconnection
                c.sendall(str(clientDisconnection).encode(FORMAT))
            break
        elif msg in users.values() and msg != username: # A node cannot chat with itself
            for guestAddr, guestUsername in users.items():
                if guestUsername == msg:
                    node.sendall(str(guestAddr).encode(FORMAT))
                    clientSocket = sockets[guestAddr]
                    clientSocket.send(f"[{users[addr]} STARTED A CHAT]".encode(FORMAT))
                    clientSocket.send(str(addr).encode(FORMAT))
                    print(f"[DISCONNECTION] {addr}: {username}")
                    clients.remove(node)
                    sockets.pop(addr)
                    users.pop(addr)
                    for c in clients: # Alerting all the nodes about the disconnection
                        if c!= clientSocket:
                            c.sendall(f"[NEW DISCONNECTION] {username}".encode(FORMAT))
                    break
            break
        else:
            node.send("[USERNAME NOT VALID]".encode(FORMAT)) # If the username entered is not valid, the node gets its socket as a flag of error

def start():
    print("[DISCOVERY SERVER STARTED]")
    newNode()


start()