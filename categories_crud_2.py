from tkinter import *
from tkinter import messagebox, ttk
import pymongo
from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000

URI = "mongodb://" + HOST + ":" + PORT + "/"

BD = "blog"
COLLECTION = "categories"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
collection = database[COLLECTION]

def mostrarDatos(name="", url=""):
    objectSearch = {}
    if len(name) != 0:
        objectSearch["name"] = name
    if len(url) != 0:
        objectSearch["url"] = url
    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        for document in collection.find(objectSearch):
            table.insert('', 0, text=document["_id"], values=(document["name"], document["url"]))
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Time exceed", err)
    except pymongo.errors.ConnectionFailure as err:
        print("Fail trying to connect to Mongodb", err)

def addCategory():
    if len(name.get()) != 0 and len(url.get()) != 0:
        try:
            document = {"name": name.get(), "url": url.get()}
            collection.insert_one(document)
            name.delete(0, END)
            url.delete(0, END)
        except pymongo.errors.ConnectionFailure as err:
            print(err)
    else:
        messagebox.showerror("Error", "Los campos no pueden estar vacíos")
    mostrarDatos()

def editCategory():
    global ID_CATEGORY
    if len(name.get()) != 0 and len(url.get()) != 0:
        try:
            idSearch = {"_id": ObjectId(ID_CATEGORY)}
            newValues = {"$set": {"name": name.get(), "url": url.get()}}
            collection.update_one(idSearch, newValues)
            name.delete(0, END)
            url.delete(0, END)
        except pymongo.errors.ConnectionFailure as err:
            print(err)
    else:
        messagebox.showerror("Error", "Los campos no pueden estar vacíos")
    mostrarDatos()
    create["state"] = "normal"
    edit["state"] = "disabled"
    delete["state"] = "disabled"

def deleteCategory():
    global ID_CATEGORY
    try:
        idSearch = {"_id": ObjectId(ID_CATEGORY)}
        collection.delete_one(idSearch)
        name.delete(0, END)
        url.delete(0, END)
    except pymongo.errors.ConnectionFailure as err:
        print(err)
    create["state"] = "normal"
    edit["state"] = "disabled"
    delete["state"] = "disabled"
    mostrarDatos()

def doubleClickTable(event):
    global ID_CATEGORY
    ID_CATEGORY = str(table.item(table.selection())["text"])
    document = collection.find({"_id": ObjectId(ID_CATEGORY)})[0]
    name.delete(0, END)
    name.insert(0, document["name"])
    url.delete(0, END)
    url.insert(0, document["url"])
    create["state"] = "disabled"
    edit["state"] = "normal"
    delete["state"] = "normal"

window = Tk()
table = ttk.Treeview(window, columns=("name", "url"))
table.grid(row=1, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("#1", text="NAME")
table.heading("#2", text="URL")
table.bind("<Double-Button-1>", doubleClickTable)

Label(window, text="Name").grid(row=2, column=0)
name = Entry(window)
name.grid(row=2, column=1, sticky=W+E)
name.focus()

Label(window, text="URL").grid(row=3, column=0)
url = Entry(window)
url.grid(row=3, column=1, sticky=W+E)

create = Button(window, text="Add Category", command=addCategory, bg="green", fg="white")
create.grid(row=5, columnspan=2, sticky=W+E)

edit = Button(window, text="Edit Category", command=editCategory, bg="yellow")
edit.grid(row=6, columnspan=2, sticky=W+E)
edit["state"] = "disabled"

delete = Button(window, text="Delete Category", command=deleteCategory, bg="red", fg="white")
delete.grid(row=7, columnspan=2, sticky=W+E)
delete["state"] = "disabled"

Label(window, text="Search for name").grid(row=8, column=0)
searchName = Entry(window)
searchName.grid(row=8, column=1, sticky=W+E)

Label(window, text="Search for URL").grid(row=9, column=0)
searchURL = Entry(window)
searchURL.grid(row=9, column=1, sticky=W+E)

search = Button(window, text="Search Category", command=lambda: mostrarDatos(searchName.get(), searchURL.get()), bg="blue", fg="white")
search.grid(row=11, columnspan=2, sticky=W+E)

mostrarDatos()

window.mainloop()