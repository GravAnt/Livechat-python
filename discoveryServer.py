import time
import socket
import threading
import account
import connDB
import bcrypt

PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = "utf-8"
DISCONN_MESSAGE = "!DISCONNECT"
REPORT_MESSAGE = "!REPORT"
MAX_REPORTS = 3
SHUT_COUNTDOWN = 100


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

serverRunning = True
clients = set() # To keep track of all the clients connected
sockets = dict() # To associate each address to socket
users = dict() # To associate each address to username

newAccounts = dict() # Due to a bug, a new account cannot reconnect to the discovery server unless the server restarts,
# so newAccounts keeps track of all the new users and to make the server allow the reconnection


def newNode():
    global newAccounts
    server.listen()
    while serverRunning:
        try:
            newUser = False
            node, addr = server.accept()
            signOrLog = node.recv(1024).decode(FORMAT)
            time.sleep(0.5)
            accountData = node.recv(1024).decode(FORMAT)
            separatorIndex = accountData.index("|")
            username = accountData[:separatorIndex]
            password = accountData[separatorIndex+1:]
            validUsername = False
            if signOrLog == "SIGNUP":
                newUser = True
                passwordCopy = password
                password = bcrypt.hashpw(password.encode(FORMAT), bcrypt.gensalt()).decode(FORMAT)
                validUsername = account.signUp(username, password)
                if validUsername:
                    newAccounts[username] = passwordCopy
            if username in newAccounts.keys() and password == newAccounts[username]:
                newUser = True
            if account.login(username, password) or newUser:
                node.send("YES_AUTH".encode(FORMAT))
                users[addr] = username
                sockets[addr] = node
                nodesConnected = "\n[NODES CONNECTED]"
                for clientAddr, clientUsername in users.items():
                    nodesConnected += "\n" + clientUsername
                print(f"[NEW CONNECTION] {addr}: {username}")
                time.sleep(0.5) # Waiting so that the connected node can receive the message as well
                clients.add(node)
                for c in clients:
                    c.sendall(nodesConnected.encode(FORMAT))
                nodeHandlingThread = threading.Thread(target=nodeHandling, args=(node, addr, username))
                nodeHandlingThread.start()
            else:
                node.send("NO_AUTH".encode(FORMAT))
                print(f"[AUTH ERROR] {addr}")

        except socket.error: # Expection occurrs after the shutdown of the server
            print("[SERVER CLOSED]")
     

def nodeDisconnection(node, addr, username):
    print(f"[DISCONNECTION] {addr}: {username}")
    clients.remove(node)
    sockets.pop(addr)
    clientDisconnection = "[NEW DISCONNECTION] " + users.pop(addr)
    node.close()
    for c in clients: # Notifying the other nodes about the disconnection
        c.sendall(str(clientDisconnection).encode(FORMAT))


def userBan(userReported):
    for address, username in users.items():
        if userReported == username:
            node = sockets[address]
            node.send("BAN_MSG".encode(FORMAT))
            print(f"[NEW BAN] {address}")
            for c in clients:
                    c.sendall(f"[{userReported} BANNED]".encode(FORMAT))
            break


def nodeHandling(node, addr, username):
    while serverRunning:
        try:
            msg = node.recv(1024).decode(FORMAT)
            if msg == DISCONN_MESSAGE:
                nodeDisconnection(node, addr, username)
                break
            elif REPORT_MESSAGE in msg:
                userReported = msg[msg.index(" ")+1:]
                totalReports = connDB.newReport(userReported)
                if totalReports == MAX_REPORTS:
                    userBan(userReported)
            elif msg in users.values() and msg != username: # A node cannot chat with itself
                for guestAddr, guestUsername in users.items():
                    if guestUsername == msg:
                        node.sendall(str(guestAddr).encode(FORMAT))
                        clientSocket = sockets[guestAddr]
                        clientSocket.send(f"[{users[addr]} STARTED A CHAT]".encode(FORMAT))
                        clientSocket.send(str(addr).encode(FORMAT))
                        print(f"[DISCONNECTION] {addr}: {username}")
                        clients.remove(node)
                        sockets.pop(addr)
                        users.pop(addr)
                        for c in clients: # Alerting all the nodes about the disconnection
                            if c!= clientSocket:
                                c.sendall(f"[NEW DISCONNECTION] {username}".encode(FORMAT))
                        break
                break
            else:
                node.send("[USERNAME NOT VALID]".encode(FORMAT)) # If the username entered is not valid, the node gets its socket as a flag of error
        except socket.error:
            nodeDisconnection(node, addr, username)
            break


def serverShutdown():
    global serverRunning
    while serverRunning:
        time.sleep(SHUT_COUNTDOWN)
        if len(clients) == 0:
            connDB.closeConn()
            server.close()
            serverRunning = False


def main():
    print("[DISCOVERY SERVER STARTED]")
    newNodeThread = threading.Thread(target=newNode)
    newNodeThread.start()
    serverShutdown()


if __name__ == "__main__":
    main()