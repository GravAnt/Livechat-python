import psycopg2

DB_HOST = "localhost"
DB_NAME = "livechat_users"
DB_USER = "postgres"
DB_PASS = "admin"

conn = psycopg2.connect(dbname = DB_NAME, user = DB_USER, password = DB_PASS, host = DB_HOST)
cur = conn.cursor()
users = list()

class User:
    def __init__(self, name, code, password, reports):
        self.name = name
        self.code = code
        self.password = password
        self.reports = reports
    
    def getName(self):
        return self.name

    def getCode(self):
        return self.code

    def getPassword(self):
        return self.password

    def getReports(self):
        return self.reports
    

def loadUsers():
    global users
    cur.execute("SELECT COUNT(*) FROM client")
    numPeople = str(cur.fetchone())
    numPeople = int(numPeople[1:len(numPeople)-2])
    # Inserting the data stored in the DB into the list
    for i in range(numPeople):
        comm = "SELECT username FROM client WHERE code = " + str(i)
        cur.execute(comm)
        username = str(cur.fetchone())
        username = username[2:-3]
        password = "SELECT password FROM client WHERE code = " + str(i)
        cur.execute(comm)
        password = str(cur.fetchone())
        password = password[2: -3]
        comm = "SELECT reports FROM client WHERE code = " + str(i)
        cur.execute(comm)
        reports = str(cur.fetchone())
        reports = int(reports[1:-2])
        users.append(User(username, i, password, reports))

    return users