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
    addrMsg = "\n[NODES CONNECTED]"
    while True:
        node, addr = server.accept()
        username = node.recv(1024).decode(FORMAT)
        users[addr] = username
        sockets[addr] = node
        addrMsg += "\n" + username
        print(f"[NEW CONNECTION] {addr}: {username}")
        time.sleep(0.5) # Waiting so that the connected node can receive the message as well
        clients.add(node)
        for c in clients:
            c.sendall(addrMsg.encode(FORMAT))
        thread = threading.Thread(target=nodeHandling, args=(node, addr, username))
        thread.start()
        

def nodeHandling(node, addr, username):
    while True:
        msg = node.recv(1024).decode(FORMAT)
        if msg == DISCONN_MESSAGE:
            print(f"[DISCONNECTION] {addr}")
            clients.remove(node)
            sockets.pop(addr)
            clientDisconnection = "[NEW DISCONNECTION] " + users.pop(addr)
            node.close()
            for c in clients: # Notifying the nodes on the disconnection
                c.sendall(str(clientDisconnection).encode(FORMAT))
            break
        elif msg in users.values():
            for clientAddr, value in users.items(): #guestAddr instead of clientAddr
                if value == msg:
                    node.sendall(str(clientAddr).encode(FORMAT))
                    clientSocket = sockets[clientAddr]
                    clientSocket.send(f"[{users[addr]} STARTED A CHAT]".encode(FORMAT))
                    clientSocket.send(str(addr).encode(FORMAT))
                    print(f"[DISCONNECTION] {addr}")
                    for c in clients: # Notifying the nodes on the disconnection
                        c.sendall(f"[NEW DISCONNECTION] {username}".encode(FORMAT))
                    #clients.remove(node)
                    #sockets.pop(addr)
                    #users.pop(addr)
                    #clients.remove(clientSocket)
                    #sockets.pop(clientAddr)
                    #users.pop(clientAddr)
                    break
            break
        else:
            node.send("[USERNAME NOT VALID]".encode(FORMAT)) # If the username entered is not valid, the node gets its socket as a flag of error

def start():
    print("[DISCOVERY SERVER STARTED]")
    newNode()


start()