import sqlite3
from os.path import isfile

class faceDB:
    def __init__(self):
        self.db = "friend.db"

    def setDBname(self, dbname):
        if ".db" in dbname:
            self.db = dbname
        else:
            self.db = dbname + ".db"

    def create(self):
        if not isfile(self.db):
            conn = sqlite3.connect(self.db)
            conn.execute('''CREATE TABLE Facebook 
                            (ID INTEGER PRIMARY KEY, NAME TEXT, LINK TEXT, COM_FRD INT)''')
            print("Create database : " + self.db + " successfully !")
            conn.close()
        else:
            print("Loading database : " + self.db + " for working !")

    def insert(self, id_list):
        conn = sqlite3.connect(self.db)
        print("Open database for Inserting !!!!")
        sql_insert_cmd = 'INSERT INTO Facebook (NAME, LINK, COM_FRD) VALUES (?, ?, ?)'
        conn.executemany(sql_insert_cmd, id_list)
        conn.commit()
        conn.close()

    def fetchall(self):
        conn = sqlite3.connect(self.db)
        print("Open database for FETCH ALL information !!!!")
        cur = conn.execute('SELECT ID, NAME, LINK, COM_FRD from Facebook')
        for obj in cur:
            print("ID : " + str(obj[0]) + " --- Name : " + obj[1] + " --- Link : " + obj[2] + " --- ComFriend + " + str(obj[3]))
        conn.close()

    def delete(self, id_list):
        conn = sqlite3.connect(self.db)
        for id in id_list:
            print("Deleting from database with ID = " + str(id))
            conn.execute('DELETE from Facebook WHERE ID= ?', (id,))

        cur = conn.execute("SELECT ID from Facebook")
        id_temp = 1
        for obj in cur:
            conn.execute('UPDATE Facebook SET ID = ? WHERE ID = ?', (id_temp, obj[0]))
            id_temp = id_temp + 1
        conn.commit()
        conn.close()

    def get_email_by_id(self, id_list):
        email = []
        conn = sqlite3.connect(self.db)
        for id in id_list:
            cur = conn.execute('SELECT LINK from Facebook WHERE ID = ?', (id,))
            for obj in cur:
                email.append(obj[0])
        conn.close()
        return email
