from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId
import pymongo.errors
HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000
URI = "mongodb://" + HOST + ":" + PORT + "/"
BD = "blog"
COLLECTION = "users"
client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
colection = database[COLLECTION]

def mostrarDatos(name="", email=""):
    objectSearch={}
    if len(name) != 0:
        objectSearch["name"]=name
    if len(email) != 0:
        objectSearch["email"]=email
    try: 
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        for document in colection.find(objectSearch):
            table.insert('', 0, text=document["_id"], values=(document["name"], document["email"]))
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Time exceed",err)
    except pymongo.errors.ConnectionFailure as err:
        print("Fail trying to connect to Mongodb",err)

def addUser():
    if len(name.get())!=0 and len(email.get())!=0:
        try:
            document={"name":name.get(), "email":email.get()}
            colection.insert_one(document)
            name.delete(0, END)
            email.delete(0, END)
        except pymongo.errors.ConnectionFailure as err:
            print(err)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
    mostrarDatos()

def doubleClickTable(event):
    global ID_USER
    ID_USER=str(table.item(table.selection())["text"])
    #print(ID_USER)
    document = colection.find({"_id":ObjectId(ID_USER)})[0]
    #print(document)
    name.delete(0, END)
    name.insert(0, document["name"])
    email.delete(0, END)
    email.insert(0, document["email"])
    create["state"]="disabled"
    edit["state"]="normal"
    delete["state"]="normal"
def editRegister():
    global ID_USER
    if len(name.get())!=0 and len(email.get())!=0:
        try:
            idSearch={"_id":ObjectId(ID_USER)}
            newValues={"$set": {"name":name.get(), "email":email.get()}}
            colection.update_one(idSearch, newValues)
            name.delete(0, END)
            email.delete(0, END)
        except pymongo.errors.ConnectionFailure as err:
            print(err)
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()
    create["state"]="normal"
    edit["state"]="disabled"
    delete["state"]="disabled"
    
def deleteRegister():
    global ID_USER
    try:
        idSearch={"_id":ObjectId(ID_USER)}
        colection.delete_one(idSearch)
        name.delete(0, END)
        email.delete(0, END)
    except pymongo.errors.ConnectionFailure as err:
        print(err)
    create["state"]="normal"
    edit["state"]="disabled"
    delete["state"]="disabled"
    mostrarDatos()
def searchRegister():
    mostrarDatos(searchName.get(), searchEmail.get())
window = Tk()
table = ttk.Treeview(window, columns=("email", "name"))
table.grid(row=1, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("#1", text="NAME")
table.heading("#2", text="EMAIL")
table.bind("<Double-Button-1>", doubleClickTable)
def on_closing():
    client.close()
    window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)
#Name
Label(window, text="Name").grid(row = 2, column = 0)
name = Entry(window)
name.grid(row = 2, column = 1, sticky=W+E)
name.focus()

Label(window, text="Email").grid(row = 3, column = 0)
email = Entry(window)
email.grid(row = 3, column = 1, sticky=W+E)

create = Button(window, text = "Add user", command=addUser, bg="green", fg="white")
create.grid(row=5, columnspan=2, sticky=W+E)

edit = Button(window, text="Edit user", command=editRegister, bg="yellow")
edit.grid(row=6, columnspan=2, sticky=W+E)
edit["state"]="disabled"
mostrarDatos()

delete = Button(window, text="Delete user", command=deleteRegister, bg="red", fg="white")
delete.grid(row=7, columnspan=2, sticky=W+E)
delete["state"]="disabled"

Label(window, text="Search for name").grid(row = 8, column = 0)
searchName = Entry(window)
searchName.grid(row = 8, column = 1, sticky=W+E)

Label(window, text="Search for Email").grid(row = 9, column = 0)
searchEmail = Entry(window)
searchEmail.grid(row = 9, column = 1, sticky=W+E)
search = Button(window, text="Search user", command=searchRegister, bg="blue", fg="white")
search.grid(row=11, columnspan=2, sticky=W+E)
mostrarDatos()

window.mainloop()