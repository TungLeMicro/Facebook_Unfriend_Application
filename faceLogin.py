from tkinter import *
from tkinter import messagebox
from faceBrowser import faceBroswer

class faceLogin:
    def __init__(self, root, browser):
        self.parent = root
        self.browser = browser
        self.lg_status = 0

    def login(self):
        mainframe = LabelFrame(self.parent, text="Login Facebook")
        mainframe.pack(padx=200, pady=200)
        loginframe = Frame(mainframe)
        loginframe.pack()
        Label(loginframe, text="Username : ").grid(row=0, column=0)
        Label(loginframe, text="Password : ").grid(row=1, column=0)
        i_user = Entry(loginframe, width=20)
        i_user.grid(row=0, column=1)
        i_user.insert(END, "lbtung28@gmail.com")
        i_pass = Entry(loginframe, width=20, show="*")
        i_pass.grid(row=1, column=1)
        i_pass.insert(END, "Password12345")
        Button(mainframe, text="Login", command=lambda: self.submit(i_user.get(), i_pass.get())).pack()

    def submit(self, usr, pwd):
        self.lg_status = faceBroswer.loginbrowser(self.browser, usr, pwd)
        if self.lg_status == 0:
            messagebox.showerror("Error", "Username or Password is wrong !!!")




