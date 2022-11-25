import connDB

def login(username, password):
    users = connDB.loadUsers()
    usernameFound = False
    passwordFound = False
    for i in range(len(users)):
        if username == users[i].getName():
            usernameFound = True
            break
    for i in range(len(users)):
        if password == users[i].getPassword():
            passwordFound = True
            break
    if usernameFound and passwordFound:
        return True
    else:
        return False

# def signin():