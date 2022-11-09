# Usa un DB per il caricamento degli utenti nel dizionario

class User:
    def __init__(self, name, password):
        self.name = name
        self.password = password
    
    def getName(self):
        return self.name

    def getPassword(self):
        return self.password

def loadUsers(): # Devo caricarli dal DB, devo anche inserire la registrazione
    users = {
        "Prova":"Prova",
        "Test":"Test",
        "Ciao":"Ciao",
        "Hi":"Hi"
    }

    return users

def main():
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

main()