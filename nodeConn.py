import socket
DISCOV_SERVER = "localhost"
DISCOV_PORT = 5050
DISCOV_ADDR = (DISCOV_SERVER, DISCOV_PORT)
FORMAT = "utf-8"
DISCONN_MESSAGE = "!DISCONNECT"

node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main():
    try: 
        username = input("Enter your username: ")
        node.connect(DISCOV_ADDR)
        node.send(username.encode(FORMAT))
        print("[CONNECTED TO THE DISCOVERY SERVER]")
        connected = True
        while connected:
            msg = node.recv(1024).decode(FORMAT)
            print(msg)
            newConn = input(f"Enter the name of the user you want to chat with, or enter {DISCONN_MESSAGE} to leave: ")
            if newConn == DISCONN_MESSAGE:
                connected = False
                node.send(newConn.encode(FORMAT))
                node.close()
    except socket.error:
        print("[UNABLE TO CONNECT TO DISCOVERY SERVER]")

    print("[LEAVING THE CHAT]")

if __name__ == "__main__":
    main()