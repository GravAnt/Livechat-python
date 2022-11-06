import socket, errno

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def start():
    portUsed = False
    try:
        node.bind(ADDR)
    except socket.error as err:
        portUsed = True
        if err.errno == errno.EADDRINUSE:
            print("[CONNECTED]")
        else:
            print("[ERROR]")
    
    return portUsed

def handle_node(conn, addr):
    try: # try ignores exceptions
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT) # 1024 is the length of the message
            if not msg: # If message is empty, disconnect the node
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] says: {msg}")
            
    finally:
        conn.close()

def main():
    portUsed = start()
    if portUsed: # There's already a node using the port
        node.connect(ADDR)
        while True:
            handle_node(conn, ADDR) #aggiusta, non è conn
            msg = input("Send message: ")
            node.send(msg.encode(FORMAT))

    if not portUsed:
        print("[STARTING THE CONNECTION]")
        node.listen()
        conn, addr = node.accept()
        while True:
            handle_node(conn, addr)
            msg = input("Send message: ")
            node.send(msg.encode(FORMAT))

main()