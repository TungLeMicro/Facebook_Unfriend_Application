from tkinter import *
from tkinter import ttk
from faceDB import faceDB
from faceBrowser import faceBroswer
import sqlite3

class faceFriend:
    def __init__(self, root, dbname, browser):
        self.parent = root
        self.db =dbname
        self.browser = browser

    def initFriendList(self):
        for child in self.parent.winfo_children():
            child.destroy()
        wrap_1 = LabelFrame(self.parent, text="Information")
        wrap_2 = LabelFrame(self.parent, text="Friend Table")
        wrap_1.pack(padx=2, pady=2, fill=BOTH, expand=YES)
        wrap_2.pack(padx=2, pady=2, fill=BOTH, expand=YES)

        appframe = LabelFrame(wrap_1, text="Application information")
        appframe.pack(side=LEFT, fill=BOTH, expand=YES)
        Label(appframe, text="Facebook Friend Management Application").grid(row=0, column=0, sticky="w")
        Label(appframe, text="Author: Tung Le").grid(row=1, column=0, sticky="w")
        Label(appframe, text="Date: July 18, 2021").grid(row=2, column=0, sticky="w")

        psframe = LabelFrame(wrap_1, text="Persional information")
        psframe.pack(side=LEFT, fill=BOTH, expand=YES)
        Label(psframe, text="FB Name : Tung Le").grid(row=0, column=0, sticky="w")
        Label(psframe, text="Address: Long An").grid(row=1, column=0, sticky="w")

        menuframe = Frame(wrap_2)
        menuframe.pack(fill=X, padx=2, pady=2)
        title = [["ID", 5], ["NAME", 20], ["LINK", 55], ["SELECT", 15]]
        for i in range(len(title)):
            entry = Entry(menuframe, width=title[i][1])
            entry.grid(row=0, column=i)
            entry.insert(END, title[i][0])
            entry.configure(state="readonly", relief=RAISED)

        fr_canvas = Canvas(wrap_2)
        fr_canvas.pack(side=LEFT, fill=BOTH, expand=YES)

        yscrollbar = ttk.Scrollbar(wrap_2, orient="vertical", command=fr_canvas.yview)
        yscrollbar.pack(side=RIGHT, fill=Y)
        fr_canvas.configure(yscrollcommand=yscrollbar.set)
        fr_canvas.bind('<Configure>', lambda e: fr_canvas.configure(scrollregion=fr_canvas.bbox("all")))
        fr_canvas.bind('<MouseWheel>', lambda e: fr_canvas.yview_scroll(int(-1*(e.delta/120)), 'units'))

        dataframe = Frame(fr_canvas)
        fr_canvas.create_window((0, 0), window=dataframe, anchor="nw")

        conn = sqlite3.connect(self.db)
        cur = conn.execute('SELECT ID, NAME, LINK from Facebook')
        row = 0
        self.sel = [""]
        self.unfbox = [""]
        for obj in cur:
            for i in range(len(obj)):
                entry = Entry(dataframe, width=title[i][1])
                entry.grid(row=row, column=i)
                entry.insert(END, obj[i])
                entry.configure(state="readonly")
            id  = obj[0]
            self.sel.append(IntVar())
            self.unfbox.append("")
            self.unfbox[id] = Checkbutton(dataframe, variable=self.sel[id])
            self.unfbox[id].grid(row=row, column=3)
            row = row + 1
        Button(self.parent, text="Unfriend", width=15, command=self.unfriend).pack(side=LEFT, fill=Y, padx=2, pady=2)
        Button(self.parent, text="Refresh", width=15, command=self.refresh).pack(side=LEFT, fill=Y, padx=2, pady=2)
        Button(self.parent, text="Clear Select", width=15, command=self.unsel_all).pack(side=LEFT, fill=Y, padx=2, pady=2)
        Button(self.parent, text="Auto Select", width=15, command=self.auto_select).pack(side=LEFT, fill=Y, padx=2, pady=2)

    def unfriend(self):
        id_list = []
        for i in range(1, len(self.sel)):
            if self.sel[i].get() == 1:
                id_list.append(i)
        if len(id_list):
            db = faceDB()
            db.setDBname(self.db)
            email = db.get_email_by_id(id_list)
            faceBroswer.unfriend_by_email(self.browser, email)
            db.delete(id_list)

    def refresh(self):
        self.initFriendList()

    def unsel_all(self):
        for i in range(1, len(self.sel)):
            self.unfbox[i].deselect()

    def auto_select(self):
        conn = sqlite3.connect(self.db)
        cur = conn.execute('SELECT ID, NAME, COM_FRD from Facebook')
        match = ["'", "Bro", "Vk", "Ck", "Exiter" ]
        for obj in cur:
            id = obj[0]
            if obj[2] == 0 or any(x in obj[1] for x in match):
                self.unfbox[id].select()
        conn.close()


# def close_window(callback=NONE):
#     root.destroy()
#
# root = Tk()
# root.title("Facebook Unfriend Application")
# root.geometry("650x500")
# root.protocol("WM_DELETE_WINDOW", close_window)
# fr = faceFriend(root, "dbFriend.db")
# fr.initFriendList()
# root.mainloop()


