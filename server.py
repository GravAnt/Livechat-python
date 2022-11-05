import threading
import socket

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

clients = set() # To keep track of all the clients connected
clients_lock = threading.Lock()
# Two threads can modify the same object at the same time, so we use .Lock()
# .Lock() makes it impossible to modify an object (in this case, a set) while another thread is acting

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} Connected")
    try: # try ignores exceptions
        connected = True
        while connected:
            msg = conn.recv(1024).decode(FORMAT) # 1024 is the length of the message
            if not msg: # If message is empty, disconnect the client
                break

            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            with clients_lock:
                for c in clients:
                    c.sendall(f"[{addr}] {msg}".encode(FORMAT))
    
    finally:
        with clients_lock:
            clients.remove(conn) # After the disconnection, the client is removed from the set
        conn.close()

def start():
    print("[SERVER STARTED]")
    server.listen() # Start listening on the address ADDR
    while True:
        conn, addr = server.accept() # conn is a socket, addr is the ip address and the port of client
        with clients_lock: # with statement ensures acquisition and release of resources
            clients.add(conn)
            # After a new client is added to the set, the with statement unlocks the thread
        # Thread is used in order to not block other clients to send messages
        thread = threading.Thread(target=handle_client, args=(conn, addr)) 
        thread.start()

start()