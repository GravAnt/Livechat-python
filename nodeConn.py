import socket
import threading
import time
import p2p
DISCOV_SERVER = "localhost"
DISCOV_PORT = 5050
DISCOV_ADDR = (DISCOV_SERVER, DISCOV_PORT)
FORMAT = "utf-8"
DISCONN_MESSAGE = "!DISCONNECT"

node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
connectedToServer = False
peersConnRequest = False
isHost = False
hostAddr = None
guestAddr = None
peerUsername = None


def receiveFromPeer(guestSocket, addr):
    while True:
        msg = guestSocket.recv(1024).decode(FORMAT) # 1024 is the length of the message
        if not msg: # If message is empty, disconnect the client
            break
        if msg == DISCONN_MESSAGE:
            break
        print(peerUsername + ": " + msg)
    
    print(peerUsername + " disconnected")


def sendToPeer():
    while True:
        try:
            msg = input("Send message: ")
            node.send(msg.encode(FORMAT))
            if msg == DISCONN_MESSAGE:
                break
        except:
            break

    print("Disconnected")


def startHosting(guestAddr):
    node.listen()
    guestSocket, guestAddr = node.accept()
    if guestAddr == guestAddr:
        print("[CONNECTED TO THE USER]")
    else:
        print("[ERROR]")

    return guestSocket, guestAddr


def connectToHost(hostAddr):
    node.connect(eval(hostAddr))
    print("[CONNECTED TO THE USER]")


def getMsg():
    global connectedToServer, peersConnRequest, isHost # Boolean global variables
    global hostAddr, clientAddr, peerUsername # Non boolean global variables
    while connectedToServer:
        try:
            msg = node.recv(1024).decode(FORMAT)
            if "[NODES CONNECTED]" in msg or "[NEW DISCONNECTION]" in msg:
                print(msg) # It prints all the users online or the username of the ones who disconnected
            else: # It means that the node got the address + port of the peer, or that someone wants to connect to the node
                if "STARTED A CHAT]" in msg: 
                    print(msg) 
                    peerUsername = msg[:msg.index("[")]
                    hostAddr = node.recv(1024).decode(FORMAT) # So the target node gets the address of the host
                    node.send(DISCONN_MESSAGE.encode(FORMAT))
                else:
                    node.send(DISCONN_MESSAGE.encode(FORMAT))
                    isHost = True
                    clientAddr = msg
                    print("[INPUT VALID]") # Otherwise the node could see the IP address of its peer
                connectedToServer = False
                peersConnRequest = True
        except socket.error:
            print("Exception")
            connectedToServer = False


def setConn():
    global connectedToServer, peerUsername
    while connectedToServer:
        try:
            if connectedToServer: # In order to avoid the displaying of the input message after the disconnection from the server
                peerUsername = input("[INPUT] ")
            node.send(peerUsername.encode(FORMAT))
            if peerUsername == DISCONN_MESSAGE:
                connectedToServer = False
        except socket.error:
            connectedToServer = False


def main():
    global node, connectedToServer
    try: 
        username = input("[ENTER YOUR USERNAME] ")
        node.connect(DISCOV_ADDR)
        node.send(username.encode(FORMAT))
        print("[CONNECTED TO THE DISCOVERY SERVER]")
        print("[WHEN ASKED FOR AN INPUT, ENTER THE NAME OF A USER TO CHAT WITH]")
        print(f"[ENTER {DISCONN_MESSAGE} TO LEAVE THE SERVER]\n")
        connectedToServer = True
        getMsgThread = threading.Thread(target=getMsg)
        setConnThread = threading.Thread(target=setConn)
        getMsgThread.start()
        setConnThread.start()
        
        while True:
            if not connectedToServer and peersConnRequest:
                print("[ATTEMPTING TO CONNECT TO THE NODE]")
                break
            elif not connectedToServer and not peersConnRequest:
                print("[GOODBYE]")
                break

        if peersConnRequest:
            myAddr = node.getsockname()
            node.close()
            node = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            node.bind(myAddr)
            if isHost:
                guestSocket, addr = startHosting(guestAddr)
            else:
                connectToHost(hostAddr)
            receiveFromPeerThread = threading.Thread(target=receiveFromPeer, args=(guestSocket, addr))
            sendToPeerThread = threading.Thread(target=sendToPeer)
            receiveFromPeerThread.start()
            sendToPeerThread.start()
            
    except socket.error:
        print("[UNABLE TO CONNECT TO THE DISCOVERY SERVER]")


if __name__ == "__main__":
    main()