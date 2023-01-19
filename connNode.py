import socket
import threading
import time
import os

node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

DISCOV_SERVER = "X.X.X.X" # Public IP of the server
DISCOV_PORT = 5006
DISCOV_ADDR = (DISCOV_SERVER, DISCOV_PORT)
FORMAT = "utf-8"
DISCONN_MESSAGE = "!DISCONNECT"
REPORT_MESSAGE = "!REPORT"
SEND_FILE_MESSAGE = "!FILE"
SEGMENT_LENGTH = 1024 # Each segment has a length of 1 KB

connectedToServer = False
connectedToPeer = False
peersConnRequest = False
isHost = False
hostAddr = None
guestAddr = None
peerUsername = None

serverMessages = ["NODES CONNECTED", "NEW DISCONNECTION", "USERNAME NOT VALID", "BANNED"]

lock = threading.Lock()


def getFile(sock):
    fileDimension = int(sock.recv(SEGMENT_LENGTH).decode(FORMAT)) # Get file dimension in bytes
    numSegments = int(fileDimension/SEGMENT_LENGTH)+1
    print(f"[{peerUsername} WANTS TO SEND YOU A FILE]\n[PRESS ENTER TO CONTINUE]")
    filename = input("[INSERT FILE NAME] ")
    print("[PRESS ENTER TO CONTINUE] ")
    path = input("[INSERT A VALID PATH] ")
    try:
        myfile = open(f"{path}/{filename}", "wb")
        for i in range(numSegments):
            data = sock.recv(SEGMENT_LENGTH)
            myfile.write(data)
            print(f"[SEGMENT {str(i+1)} DOWNLOADED]")
        myfile.close()
        print("[DOWNLOAD COMPLETED]")
    except:
        print("[INVALID PATH]")


def sendFile(sock, msg):
    path = msg[msg.index(" ")+1:] # " " works as separator
    try:
        myfile = open(path, "rb")
        fileDim = os.stat(path).st_size
        sock.send(str(fileDim).encode(FORMAT)) # Peer sends the dimension of file
        time.sleep(1)
        sock.send(myfile.read())
        myfile.close()
        time.sleep(1)
        print("[FILE SENT]")
    except:
        print("[PATH NOT VALID]")


def receiveFromPeer(sock, addr):
    global connectedToPeer
    while connectedToPeer:
        msg = sock.recv(SEGMENT_LENGTH).decode(FORMAT)
        if not msg: # If message is empty, disconnect the peer
            connectedToPeer = False
        elif SEND_FILE_MESSAGE in msg:
            lock.acquire()
            getFile(sock)
            lock.release()
        elif msg == DISCONN_MESSAGE:
            sock.send(DISCONN_MESSAGE.encode(FORMAT)) # To synchronize the disconnection between two nodes
            connectedToPeer = False
        else:
            print(peerUsername + ": " + msg)
    print(f"\n[{peerUsername} DISCONNECTED]")


def sendToPeer(sock, addr):
    global connectedToPeer
    while connectedToPeer:
        try:
            msg = input()
            sock.send(msg.encode(FORMAT))
            if SEND_FILE_MESSAGE in msg:
                #lock.acquire()
                sendFile(sock, msg)
                #lock.release()
            elif msg == DISCONN_MESSAGE:
                connectedToPeer = False
        except:
            connectedToPeer = False
    print("[DISCONNECTED]")


def startHosting(guestAddr):
    global connectedToPeer
    print("[USE !DISCONNECT TO LEAVE THE CHAT]\n[USE !FILE *path* TO SEND A FILE]")
    node.listen()
    guestSocket, guestAddr = node.accept()
    if guestAddr == guestAddr:
        print("[CONNECTED TO THE USER]")
        connectedToPeer = True
    else:
        print("[ERROR]")

    return guestSocket, guestAddr


def connectToHost(hostAddr):
    global connectedToPeer
    print("[USE !DISCONNECT TO LEAVE THE CHAT]\n[USE !FILE *path* TO SEND A FILE]")
    try:
        node.connect(eval(hostAddr))
        print("[CONNECTED TO THE USER]")
        connectedToPeer = True
    except socket.error:
        print("[ERROR]")


def getMsg():
    global connectedToServer, peersConnRequest, isHost # Boolean global variables
    global hostAddr, clientAddr, peerUsername # Non boolean global variables
    while connectedToServer:
        try:
            msg = node.recv(SEGMENT_LENGTH).decode(FORMAT)
            nodeDisconnection = True
            for i in range(len(serverMessages)):
                if serverMessages[i] in msg:
                    nodeDisconnection = False
                    break
            if not nodeDisconnection:
                print(msg) # It prints all the users online or the username of the ones who disconnected
            else: # It means that the node got the address + port of the peer, or that someone wants to connect to the node
                if "STARTED A CHAT" in msg: 
                    print(msg) 
                    peerUsername = msg[:msg.index(" STARTED")]
                    peerUsername = peerUsername[1:]
                    hostAddr = node.recv(SEGMENT_LENGTH).decode(FORMAT) # So the target node gets the address of the host
                    time.sleep(0.5)
                    node.send(DISCONN_MESSAGE.encode(FORMAT))
                    connectedToServer = False
                    peersConnRequest = True
                elif "BAN MSG" in msg:
                    print("[YOU CAN NO LONGER USE YOUR ACCOUNT]")
                    connectedToServer = False
                elif "DISCONNECTED" in msg:
                    connectedToServer = False
                else:
                    node.send(DISCONN_MESSAGE.encode(FORMAT))
                    isHost = True
                    clientAddr = msg
                    connectedToServer = False
                    peersConnRequest = True
                
        except socket.error:
            print("Exception")
            connectedToServer = False


def setConn():
    global connectedToServer, peersConnRequest, peerUsername
    while connectedToServer:
        try:
            if connectedToServer: # In order to avoid the displaying of the input message after the disconnection from the server
                str = input("[INPUT] ")
                node.send(str.encode(FORMAT))
                if str != "":
                    peerUsername = str
                if str == DISCONN_MESSAGE:
                    connectedToServer = False
                    peersConnRequest = False
        except socket.error:
            connectedToServer = False


def main():
    global node, connectedToServer, peersConnRequest, myAddr
    try:
        myPrivateIP = input("[ENTER YOUR PRIVATE IP OR ENTER 0 TO GET THE IP AUTOMATICALLY (IT DOESN'T WORK ON ALL MACHINES)] ")
        myPort = input("[ENTER PORT] ")
        if myPrivateIP == "0":
            myPrivateIP = str(socket.gethostbyname(socket.gethostname()))
        myAddr = (myPrivateIP, int(myPort))
        node.bind(myAddr)
        signUp = input("[ENTER 1 TO SIGN UP, ANY OTHER KEY TO LOGIN] ") 
        username = input("[ENTER USERNAME] ")
        password = input("[ENTER PASSWORD] ")
        accountData = username + "|" + password
        mainLoop = True
        while mainLoop:
            node.connect(DISCOV_ADDR)
            if signUp == '1':
                node.send("SIGNUP".encode(FORMAT))
            else:
                node.send("LOGIN".encode(FORMAT))
            time.sleep(0.5)
            node.send(accountData.encode(FORMAT))
            auth = node.recv(SEGMENT_LENGTH).decode(FORMAT)
            if auth == "YES_AUTH":
                print("[CONNECTED TO THE DISCOVERY SERVER]")
                print("[WHEN ASKED FOR AN INPUT, ENTER THE NAME OF A USER TO CHAT WITH]")
                print(f"[YOU CAN REPORT ANY USER USING '{REPORT_MESSAGE} *username*']")
                print(f"[ENTER {DISCONN_MESSAGE} TO LEAVE THE SERVER]\n")
                connectedToServer = True
                getMsgThread = threading.Thread(target=getMsg)
                setConnThread = threading.Thread(target=setConn)
                getMsgThread.start()
                time.sleep(1)
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
                        sock, addr = startHosting(guestAddr) # Server uses the connected node's socket to send/receive messages to/from client
                    else:
                        connectToHost(hostAddr)
                        sock = node # Client uses its socket to send/receive messages to/from server
                        addr = hostAddr
                    receiveFromPeerThread = threading.Thread(target=receiveFromPeer, args=(sock, addr))
                    sendToPeerThread = threading.Thread(target=sendToPeer, args=(sock, addr))
                    receiveFromPeerThread.start()
                    sendToPeerThread.start()

                while connectedToPeer: # Waiting until the chat ends
                    continue
            
                if isHost:
                    node.close()
                if peersConnRequest: # The node can't reconnect to the discovery server if it sent a !DISCONNECT message to the server itself
                    mainLoop = input("\nPress 1 if you want to reconnect to the discovery server: ")
                else:
                    mainLoop = 0
                peersConnRequest = False
                if mainLoop:
                    node = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
            else:
                print("[WRONG CREDENTIALS]")
                node.close()
            
    except socket.error:
        print(socket.error)


if __name__ == "__main__":
    main()