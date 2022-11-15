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
connected = False

def startHosting(msg):
    node.bind(node.getsockname()) 
    node.listen()
    while True:
        print("WAITING")
        peerSocket, peerAddr = node.accept()
        if peerAddr == msg:
            print("[CONNECTED TO THE USER]")
        else:
            print("[ERROR]")

def connectToHost(hostAddr):
    node.connect(eval(hostAddr))
    print("[CONNECTED TO THE USER]")


def getMsg():
    global connected
    while connected:
        try:
            msg = node.recv(1024).decode(FORMAT)
            if "[NODES CONNECTED]" in msg or "[NEW DISCONNECTION]" in msg:
                print(msg) # It prints all the users online or the username of the ones who disconnected
            else: # It means that the node got the address + port of the peer, or that someone wants to connect to the node
                if "STARTED A CHAT]" in msg: 
                    hostAddr = node.recv(1024).decode(FORMAT) # So the target node gets the address of the host
                    node.send(DISCONN_MESSAGE.encode(FORMAT))
                    print(msg + "\n[PRESS ENTER TO CONTINUE]")
                    connectToHost(hostAddr)
                else:
                    node.send(DISCONN_MESSAGE.encode(FORMAT))
                    print("[INPUT VALID, PRESS ENTER TO CONTINUE]") # Otherwise the node could see the IP address of its peer
                    startHosting(msg)
                connected = False
        except socket.error:
            print("Exception")
            connected = False

def setConn():
    global connected
    while connected:
        try:
            newConn = input("[INPUT] ")
            node.send(newConn.encode(FORMAT))
            if newConn == DISCONN_MESSAGE:
                node.close()
                connected = False
        except socket.error:
            connected = False

def main():
    try: 
        username = input("[ENTER YOUR USERNAME] ")
        node.connect(DISCOV_ADDR)
        node.send(username.encode(FORMAT))
        print("[CONNECTED TO THE DISCOVERY SERVER]")
        print("[WHEN ASKED FOR AN INPUT, ENTER THE NAME OF A USER TO CHAT WITH]")
        print(f"[ENTER {DISCONN_MESSAGE} TO LEAVE THE SERVER]\n")
        global connected
        connected = True
        threadOne = threading.Thread(target=getMsg)
        threadTwo = threading.Thread(target=setConn)
        threadOne.start()
        threadTwo.start()


            
    except socket.error:
        print("[UNABLE TO CONNECT TO DISCOVERY SERVER]")

if __name__ == "__main__":
    main()