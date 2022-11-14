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

def getMsg():
    global connected
    while connected:
        try:
            msg = node.recv(1024).decode(FORMAT)
            if "[NODES CONNECTED]" in msg or "[NEW DISCONNECTION]" in msg:
                print(msg) # It prints all the users online or the username of the ones who disconnected
            else: # It means that the node got the address + port of the peer, or that someone wants to connect to the node
                node.send(DISCONN_MESSAGE.encode(FORMAT))
                node.close()
                if "STARTED A CHAT]" in msg: 
                    print(msg + "\n[PRESS ENTER TO CONTINUE]]")
                else:
                    print("[INPUT VALID, PRESS ENTER TO CONTINUE]") # Otherwise the node could see the IP address of its peer
                connected = False
        except socket.error:
            node.close()
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