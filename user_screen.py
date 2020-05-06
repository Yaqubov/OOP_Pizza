from tkinter import *
from decorator_pattern import *
from users import *
import sqlite3
import json

class UserScreen(Tk):
    def __init__(self,customer):
        super().__init__()
        self.config(bg="#ffa366")
        self.currentCustomer = customer
        self.currentPizza = None
        self.result = None
        self.customerUsername = Label(self,text = "Customer: " + self.currentCustomer.get_username(),bg="#ffa366",font=("Courier", 22)).pack()
        self.commonFrame = Frame(self)
        self.commonFrame.config(bg="#ffa366")
        self.commonFrame.pack()
        self.pizzaFrame = Frame(self.commonFrame)
        self.pizzaFrame.pack(side=LEFT)
        self.exFrame = Frame(self.commonFrame)
        self.exFrame.pack(side=LEFT)
        self.pizzaLabel = Label(self.pizzaFrame,text="Pizzas:",bg="#ffa366",font=("Courier", 25)).pack(fill=X)
        self.pizzalistFrame = Frame(self.pizzaFrame)
        self.pizzalistFrame.pack()
        self.pizzaList = Listbox(self.pizzalistFrame)
        self.pizzaList.config(bg="#ffa366",font=("Courier", 15))
        pizzascrollbar = Scrollbar(self.pizzalistFrame, orient="vertical")
        pizzascrollbar.config(command=self.pizzaList.yview)
        pizzascrollbar.pack(side="right", fill="y")
        file = sqlite3.connect('pizzas.db')
        c = file.cursor()
        for i in (c.execute("SELECT name FROM pizzas ")):
            self.pizzaList.insert(END,i[0])
        file.commit()
        self.pizzaList.pack(side=LEFT)
        self.selectPizzaButton = Button(self.pizzaFrame,text = "Select",command = self.selectPizza,bg="#ffa366",font=("Courier", 15)).pack(fill=X)
        self.exLabel = Label(self.exFrame,text="Extentions:",bg="#ffa366",font=("Courier", 25)).pack(fill=X)
        self.extentionlistFrame = Frame(self.exFrame)
        self.extentionlistFrame.pack()
        self.extensionsList = Listbox(self.extentionlistFrame,selectmode=MULTIPLE)
        self.extensionsList.config(bg="#ffa366",font=("Courier", 15))
        exscrollbar = Scrollbar(self.extentionlistFrame, orient="vertical")
        exscrollbar.config(command=self.extensionsList.yview)
        exscrollbar.pack(side="right", fill="y")
        file = sqlite3.connect('extentions.db')
        c = file.cursor()
        for i in (c.execute("SELECT name FROM extentions ")):
            self.extensionsList.insert(END,i[0])
        file.commit()
        self.extensionsList.pack(side=LEFT)
        self.scrollbar = Scrollbar(self, orient="vertical")
        self.buttonFrame = Frame(self.exFrame)
        self.buttonFrame.config(bg="#ffa366")
        self.buttonFrame.pack()
        self.addExtensionButton = Button(self.buttonFrame,text = "Add",command = self.addExtension,width=8,bg="#ffa366",font=("Courier", 15)).pack(side=LEFT)
        self.removeExtensionButton = Button(self.buttonFrame,text = "Remove",command = self.removeExtension,width=8,bg="#ffa366",font=("Courier", 15)).pack(side=LEFT)
        self.showOrderList = Button(self,text = "Show order history",command=self.showOrders,bg="#ffa366",font=("Courier", 15)).pack()
        self.orderButton = Button(self,text = "Order",command = self.order,bg="#ffa366",font=("Courier", 15)).pack()
        

    def showOrders(self):
        username = self.currentCustomer.get_username()
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

    def removeExtension(self):
        file = sqlite3.connect('extentions.db')
        c = file.cursor()
        file.commit()
        reslist = list()
        selections = self.extensionsList.curselection()
        for i in selections:
            current = self.extensionsList.get(i)
            reslist.append(current)
        for val in reslist:
            self.currentPizza.remove_extention(val)
        file.close()
        if (self.result != None):
            self.result.destroy()
        self.result = Text(self,bg="#ffa366",height=7,width=35)
        self.result.insert(END,self.currentPizza.get_status()+"\n")
        self.result.insert(END,"Price: " + str(self.currentPizza.get_price()))
        self.result.config(font=("Courier", 15))
        self.result.pack()
    
    def addExtension(self):
        file = sqlite3.connect('extentions.db')
        c = file.cursor()
        file.commit()
        reslist = list()
        selections = self.extensionsList.curselection()
        for i in selections:
            current = self.extensionsList.get(i)
            reslist.append(current)
        for val in reslist:
            c.execute("SELECT price FROM extentions WHERE name=?",(val,))
            self.currentPizza.add_extention(val,c.fetchone()[0])
        file.close()
        if (self.result != None):
            self.result.destroy()
        self.result = Text(self,bg="#ffa366",height=7,width=35)
        self.result.insert(END,self.currentPizza.get_status()+"\n")
        self.result.insert(END,"Price: " + str(self.currentPizza.get_price()))
        self.result.config(font=("Courier", 15))
        self.result.pack()
        
    def selectPizza(self):
        file = sqlite3.connect('pizzas.db')
        c = file.cursor()
        pizzaType = self.pizzaList.get(ANCHOR)
        c.execute("SELECT price FROM pizzas WHERE name=?",(pizzaType,))
        self.currentPizza = PizzaBuilder(pizzaType,c.fetchone()[0])
        file.commit()
        file.close()
        if (self.result != None):
            self.result.destroy()
        self.result = Text(self,bg="#ffa366",height=7,width=35)
        self.result.insert(END,self.currentPizza.get_status()+"\n")
        self.result.insert(END,"Price: " + str(self.currentPizza.get_price()))
        self.result.config(font=("Courier", 15))
        self.result.pack()
        
    
    def order(self):
        if self.result != None:
            self.result.destroy()
        self.result = Label(self,text = "Pizza: " + self.currentPizza.get_status() + "\n" + "Price: " + str(self.currentPizza.get_price()) + "\nOrdered!")
        self.result.config(bg="#ffa366",fg="red")
        file = sqlite3.connect("accounts.db")
        c = file.cursor()
        c.execute("SELECT orderlist FROM accounts WHERE username =?",(self.currentCustomer.get_username(),))
        data = json.loads(c.fetchone()[0])
        data.append("Pizza: " + self.currentPizza.get_status() + "\n" + "Price: " + str(self.currentPizza.get_price()))
        new = json.dumps(data)
        c.execute("UPDATE accounts SET orderlist=? WHERE username=?",(new,self.currentCustomer.get_username()))
        file.commit()
        file.close()
        self.result.pack()
    
