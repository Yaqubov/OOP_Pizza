from tkinter import *
from users import *
from user_screen import *
from register_screen import *
from admin_screen import *
import sqlite3

class LoginScreen(Tk):
    def __init__(self):
        super().__init__()
        self.title("Pizza order")
        self.userFrame = Frame(self)
        self.userLabel = Label(self.userFrame,width = 12,text = "Username:",anchor = 'w',bg="#ffa366")
        self.userLabel.config(font=("Courier", 22))
        self.userLabel.pack(side = LEFT)
        self.userEntry = Entry(self.userFrame,font=("Courier", 22))
        self.userEntry.pack(side = RIGHT,fill = X,expand = YES)
        self.userFrame.pack(side = TOP,fill = X,padx = 5,pady = 5)
        self.passwordFrame = Frame(self)
        self.passwordLabel = Label(self.passwordFrame,width = 12,text = "Password:",anchor = 'w',bg="#ffa366")
        self.passwordLabel.config(font=("Courier", 22))
        self.passwordLabel.pack(side = LEFT)
        self.passwordEntry = Entry(self.passwordFrame,show = "*",font=("Courier", 22))
        self.passwordEntry.pack(side = RIGHT,fill = X,expand = YES)
        self.passwordFrame.pack(side = TOP,fill = X,padx = 5,pady = 5)
        self.loginButton = Button(self,text = "Log in",command = self.loginClick,bg="#ffa366",width = 15,height = 2,font=("Courier", 15)).pack(side = LEFT,padx = 5,pady = 5)
        self.registerButton = Button(self,text = "Register",command = self.registerClick,bg="#ffa366",width = 15,height = 2,font=("Courier", 15)).pack(side = RIGHT,padx = 5,pady = 5)
        self.successLabel = None

    def loginClick(self):
        username = self.userEntry.get()
        password = self.passwordEntry.get()
        state = False
        if(username == "admin" and password == "admin"):
            adminscreen = AdminScreen()
            self.destroy()
            adminscreen.title("Admin Screen")
            adminscreen.geometry("+600+300")
            adminscreen.configure(bg="#ffa366")
            adminscreen.mainloop()
        
        file = sqlite3.connect("accounts.db")
        c = file.cursor()
        c.execute("SELECT username, password FROM accounts WHERE username=? AND password=?",(username,password))
        if c.fetchone() != None:
            state = True

        if(state):
            screen = UserScreen(Customer(self.userEntry.get(),self.passwordEntry.get()))
            self.destroy()
            screen.title("User Screen")
            screen.geometry("+600+300")
            screen.configure(bg="#ffa366")
            screen.mainloop()
        else:
            if self.successLabel != None:
                self.successLabel.destroy()
            self.successLabel = Label(self,text = "Sorry,try again",fg = "red")
            self.successLabel.pack()
    
    def registerClick(self):
        registerScreen(self).geometry("+600+300")