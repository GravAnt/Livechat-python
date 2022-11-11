# Usa un DB per il caricamento degli utenti nel dizionario
import random
import socket

portsAssociated = dict()

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
        invalidPort = True
        while invalidPort:
            self.port = random.randint(0, 65535) # Each user gets a random port, among the available ones
            node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                addr = ("localhost", self.port)
                node.bind(addr)
                invalidPort = False
                node.close()
            except socket.error:
                continue
    
    def getName(self):
        return self.name

    def getPassword(self):
        return self.password

    def getPort(self):
        return self.port

def loadUsers(): # Devo caricarli dal DB, devo anche inserire la registrazione
    users = {
        "Prova":"Prova",
        "Test":"Test",
        "Ciao":"Ciao",
        "Hi":"Hi"
    }

    return users

def login():
    loginNotValid = True
    name = input("Enter username: ")
    psw = input("Enter password: ")
    users = loadUsers()
    while loginNotValid:
        if users.get(name) == None:
            print("Username not valid")
            name = input("Enter username: ")
        elif users.get(name) != psw:
            print("Password not valid")
            psw = input("Enter password: ")
        else:
            print("Welcome " + name)
            loginNotValid = False
    
    return name, psw

def main():
    name, psw = login()
    user = User(name, psw)
    print(user.getPort())

main()