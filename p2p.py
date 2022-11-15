import socket, threading

FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

#node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def portUsed(ADDR, node):
    portUsed = False
    try:
        node.bind(ADDR)
    except socket.error:
        portUsed = True
    
    return portUsed
    
def receiveFromPeer(node, addr):
    connected = True
    while connected:
        msg = node.recv(1024).decode(FORMAT) # 1024 is the length of the message
        if not msg: # If message is empty, disconnect the client
            break
        if msg == DISCONNECT_MESSAGE:
            connected = False
        print(f"\n[{addr}] {msg}")
    
    print(f"[DISCONNECTION] {addr}")
    node.close()
def sendToPeer(conn, addr):
    connected = True
    while connected:
        try:
            msg = input("Send message: ")
            conn.send(msg.encode(FORMAT))
        except:
            connected = False
    print(f"[ERROR] {addr} disconnected")

def main(ADDR, node):
    if not portUsed(ADDR):
        print("[LISTENING]")
        node.listen() # Start listening on the address ADDR
        conn, addr = node.accept() # conn is a socket, addr is the ip address and the port of client
        print(f"[NEW CONNECTION] {addr} Connected")
        receiveMsg = threading.Thread(target=receiveFromPeer, args=(conn, addr)) 
        receiveMsg.start()
        sendMsg = threading.Thread(target=sendToPeer, args=(conn, addr)) 
        sendMsg.start()
    
    else:
        node.connect(ADDR)
        print(f"[CONNECTED] {ADDR}")
        receiveMsg = threading.Thread(target=receiveFromPeer, args=(node, ADDR)) 
        receiveMsg.start()
        sendMsg = threading.Thread(target=sendToPeer, args=(node, ADDR)) 
        sendMsg.start()

if __name__ == "__main__":
    main()