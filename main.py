
from tkinter import *
from faceLogin import faceLogin
from faceBrowser import faceBroswer
from faceDB import faceDB
from faceFriend import faceFriend
from time import sleep
from threading import Thread
import sys
from os.path import getsize

def close_window(callback=NONE):
    lg.lg_status = 2
    root.destroy()

def getFriend():
    if getsize(dbname) < 10000:
        browser.getfriendlist()
    db.fetchall()
    friend = faceFriend(root, dbname, browser)
    friend.initFriendList()

def waiting_for_login():
    while lg.lg_status == 0:
        print("Waiting for login ...")
        sleep(2)

    if lg.lg_status == 2:
        print("Tool closing, all threads are stop !!!")
        sys.exit()

    if lg.lg_status == 1:
        print("Login successfully !!!")
        getFriend()

root = Tk()
root.title("Facebook Unfriend Application")
root.geometry("650x500")
root.protocol("WM_DELETE_WINDOW", close_window)

dbname = "dbFriend.db"

db = faceDB()
db.setDBname(dbname)
db.create()
browser = faceBroswer(db)

lg = faceLogin(root, browser)
lg.login()

thr_login = Thread(target=waiting_for_login)
thr_login.start()

root.mainloop()