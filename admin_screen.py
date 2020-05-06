from tkinter import *
import sqlite3
import json

class AdminScreen(Tk):
    def __init__(self):
        super().__init__()
        addPizzaTypeButton = Button(self,text = "Add new pizza",command = self.addPizza,bg="#ffa366",width = 20,height = 2,font=("Courier", 15))
        addExtentionButton = Button(self,text = "Add new extention",command = self.addExtention,bg="#ffa366",width = 20,height = 2,font=("Courier", 15))
        addPizzaTypeButton.pack()
        addExtentionButton.pack()
        ulist = Label(self,text = "Customers:",font=("Courier", 15),bg="#ffa366").pack()
        self.listFrame = Frame(self)
        self.listFrame.pack()
        self.userList = Listbox(self.listFrame,bg="#ffa366",height=5)
        self.userList.config(font=("Courier", 25))
        scrollbar = Scrollbar(self.listFrame, orient="vertical")
        scrollbar.config(command=self.userList.yview)
        scrollbar.pack(side="right", fill="y")
        file = sqlite3.connect('accounts.db')
        c = file.cursor()
        for i in (c.execute("SELECT username FROM accounts ")):
            self.userList.insert(END,i[0])
        file.commit()
        self.userList.pack()
        showResultButton = Button(self,text = "Show order list",command = self.showOrders,bg="#ffa366",width = 20,height = 2,font=("Courier", 15)).pack()
        self.result = None
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.exErrorLabel = None
        self.pizzaErrorLabel = None
        
    
    def showOrders(self):
        username = self.userList.get(ANCHOR)
        file = sqlite3.connect('accounts.db')
        c = file.cursor()
        c.execute("SELECT orderlist FROM accounts WHERE username=?",(username,))
        data = json.loads(c.fetchone()[0])
        if (self.result != None):
            self.result.destroy()
        self.result = Text(self,bg="#ffa366",height=10,width=35)
        self.result.config(font=("Courier", 15))
        for i in data:
            self.result.insert(END,i+"\n")
        self.scrollbar.pack(side="right", fill="y")
        self.result.pack()
        self.result.config(yscrollcommand=self.scrollbar)
        file.commit()
        file.close()
        


    def addPizza(self):
        addPizzaScreen = Toplevel(self)
        addPizzaScreen.geometry("+800+400")
        addPizzaScreen.config(bg="#ffa366")
        addPizzaScreen.title("Add Pizza")
        self.nameFrame = Frame(addPizzaScreen)
        self.nameLabel = Label(self.nameFrame,width = 12,text = "Pizza name:",bg="#ffa366",anchor = 'w')
        self.nameLabel.config(font=("Courier", 22))
        self.nameLabel.pack(side = LEFT)
        self.nameEntry = Entry(self.nameFrame,font=("Courier", 22))
        self.nameEntry.pack(side = RIGHT,fill = X,expand = YES)
        self.nameFrame.pack(side = TOP,fill = X,padx = 5,pady = 5)
        self.priceFrame = Frame(addPizzaScreen)
        self.priceLabel = Label(self.priceFrame,width = 12,text = "Pizza price:",bg="#ffa366",anchor = 'w')
        self.priceLabel.config(font=("Courier", 22))
        self.priceLabel.pack(side = LEFT)
        self.priceEntry = Entry(self.priceFrame,font=("Courier", 22))
        self.priceEntry.pack(side = RIGHT,fill = X,expand = YES)
        self.priceFrame.pack(side = TOP,fill = X,padx = 5,pady = 5)
        

        def addPizzaType():
            if self.pizzaErrorLabel != None:
                self.pizzaErrorLabel.destroy()
            f = sqlite3.connect('pizzas.db')
            c = f.cursor()
            c.execute("SELECT * FROM pizzas WHERE name=?",(self.nameEntry.get(),))
            if c.fetchone() != None:
                self.pizzaErrorLabel = Label(addPizzaScreen,text = "There is such pizza,add new one!")
                self.pizzaErrorLabel.pack()
                return
            pizzatype = self.nameEntry.get()
            price = self.priceEntry.get()
            if len(pizzatype) != 0 and len(price) != 0:
                c.execute("INSERT INTO pizzas VALUES (?,?)",(pizzatype,price))
            else:
                self.pizzaErrorLabel = Label(addPizzaScreen,text = "Sorry! Complete all sections")
                self.pizzaErrorLabel.pack()
                return
            f.commit()
            f.close()
            
            addPizzaScreen.destroy()

        addButton = Button(addPizzaScreen,text = "Add",command = addPizzaType,bg="#ffa366",width = 15,height = 2,font=("Courier", 15)).pack()
    
    def addExtention(self):
        addExtentionScreen = Toplevel(self)
        addExtentionScreen.geometry("+600+300")
        addExtentionScreen.config(bg="#ffa366")
        addExtentionScreen.title("Add Extention")
        self.nameFrame = Frame(addExtentionScreen)
        self.nameLabel = Label(self.nameFrame,width = 17,text = "Extention name:",anchor = 'w',bg="#ffa366")
        self.nameLabel.config(font=("Courier", 22))
        self.nameLabel.pack(side = LEFT)
        self.nameEntry = Entry(self.nameFrame,font=("Courier", 22))
        self.nameEntry.pack(side = RIGHT,fill = X,expand = YES)
        self.nameFrame.pack(side = TOP,fill = X,padx = 5,pady = 5)
        self.priceFrame = Frame(addExtentionScreen)
        self.priceLabel = Label(self.priceFrame,width = 17,text = "Extention price:",anchor = 'w',bg="#ffa366")
        self.priceLabel.config(font=("Courier", 22))
        self.priceLabel.pack(side = LEFT)
        self.priceEntry = Entry(self.priceFrame,font=("Courier", 22))
        self.priceEntry.pack(side = RIGHT,fill = X,expand = YES)
        self.priceFrame.pack(side = TOP,fill = X,padx = 5,pady = 5)

        def addNewExtention():
            if self.exErrorLabel != None:
                self.exErrorLabel.destroy()
            f = sqlite3.connect('extentions.db')
            c = f.cursor()
            c.execute("SELECT * FROM extentions WHERE name=?",(self.nameEntry.get(),))
            if c.fetchone() != None:
                self.exErrorLabel = Label(addExtentionScreen,text = "There is such extention,add new one!")
                self.exErrorLabel.pack()
                return
            name = self.nameEntry.get()
            price = self.priceEntry.get()
            if len(name) != 0 and len(price) != 0:
                c.execute("INSERT INTO extentions VALUES (?,?)",(name,price))
            else:
                self.exErrorLabel = Label(addExtentionScreen,text = "Sorry! Complete all sections")
                self.exErrorLabel.pack()
                return 
            f.commit()
            f.close()
            addExtentionScreen.destroy()

        addExtentionButton = Button(addExtentionScreen,text = "Add",command = addNewExtention,bg="#ffa366",width = 15,height = 2,font=("Courier", 15)).pack()
