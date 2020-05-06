from tkinter import *
import sqlite3

class registerScreen(Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.configure(bg="#ffa366")
        self.title("Register")
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
        self.registerButton = Button(self,text = "Register", command = self.register,bg="#ffa366",width = 15,height = 2,font=("Courier", 15)).pack()
    
    def register(self):
        file = sqlite3.connect('accounts.db')
        c = file.cursor()
        c.execute("SELECT * FROM accounts WHERE username=?",(self.userEntry.get(),))

        if c.fetchone() != None:
            errorLabel = Label(self,text = "There is such username,change it!")
            errorLabel.grid(row = 3)
            return
        
        c.execute("INSERT INTO accounts VALUES (?,?,?)",(self.userEntry.get(),self.passwordEntry.get(),"[]"))
        file.commit()
        file.close()
        self.destroy()
        
        

