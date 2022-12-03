import connDB
import bcrypt

FORMAT = 'utf-8'


def login(username, password):
    usersList, numPeople = connDB.loadUsers()
    usernameFound = False
    passwordFound = False
    for i in range(numPeople):
        if username == usersList[i].getName():
            usernameFound = True
            break
    for i in range(numPeople):
        if bcrypt.checkpw(password.encode(FORMAT), usersList[i].getPassword().encode(FORMAT)):
            passwordFound = True
            break
    if usernameFound and passwordFound:
        return True
    else:
        return False


def signUp(username, password):
    validUsername = True
    usersList, numPeople = connDB.loadUsers()
    for i in range(numPeople):
        if username == usersList[i].getName():
            validUsername = False
            break
    if validUsername:
        connDB.insertUsers(username, password)

    return validUsername