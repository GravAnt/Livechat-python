import socket
import threading
import time
DISCOV_SERVER = "localhost"
DISCOV_PORT = 5050
DISCOV_ADDR = (DISCOV_SERVER, DISCOV_PORT)
FORMAT = "utf-8"
DISCONN_MESSAGE = "!DISCONNECT"

node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def getMsg():
    while True:
        try:
            msg = node.recv(1024).decode(FORMAT)    # L'ADDRESS DEL PEER LO PRENDE DA QUA
            print(msg + " diocane")
        except socket.error:
            break

def setConn():
    while True:
        newConn = input(f"Enter the name of the user you want to chat with, or enter {DISCONN_MESSAGE} to leave: ")
        node.send(newConn.encode(FORMAT))
        if newConn == DISCONN_MESSAGE:
            node.close()
            break

def main():
    try: 
        username = input("Enter your username: ")
        node.connect(DISCOV_ADDR)
        node.send(username.encode(FORMAT))
        print("[CONNECTED TO THE DISCOVERY SERVER]")
        threadOne = threading.Thread(target=getMsg)
        threadTwo = threading.Thread(target=setConn)
        threadOne.start()
        threadTwo.start()
            
    except socket.error:
        print("[UNABLE TO CONNECT TO DISCOVERY SERVER]")

if __name__ == "__main__":
    main()