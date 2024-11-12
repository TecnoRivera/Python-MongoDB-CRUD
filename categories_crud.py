# categories_crud.py
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

def mostrarCategorias():
    try:
        for document in collection.find():
            table.insert('', 0, text=document["_id"], values=(document["name"], document["url"]))
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Tiempo excedido:", err)
    except pymongo.errors.ConnectionFailure as err:
        print("Error de conexión a MongoDB:", err)

def addCategory():
    if len(name.get()) != 0 and len(url.get()) != 0:
        try:
            document = {"name": name.get(), "url": url.get()}
            collection.insert_one(document)
        except pymongo.errors.ConnectionFailure as err:
            print("Error:", err)
    mostrarCategorias()

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
            print("Error:", err)
    mostrarCategorias()

def deleteCategory():
    global ID_CATEGORY
    try:
        idSearch = {"_id": ObjectId(ID_CATEGORY)}
        collection.delete_one(idSearch)
    except pymongo.errors.ConnectionFailure as err:
        print("Error:", err)
    mostrarCategorias()

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
table.grid(row=0, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("name", text="Name")
table.heading("url", text="URL")
table.bind("<Double-1>", doubleClickTable)

Label(window, text="Name").grid(row=1, column=0)
name = Entry(window)
name.grid(row=1, column=1, sticky=W+E)

Label(window, text="URL").grid(row=2, column=0)
url = Entry(window)
url.grid(row=2, column=1, sticky=W+E)

create = Button(window, text="Add Category", command=addCategory, bg="green")
create.grid(row=3, columnspan=2, sticky=W+E)

edit = Button(window, text="Edit Category", command=editCategory, bg="yellow")
edit.grid(row=4, columnspan=2, sticky=W+E)
edit["state"] = "disabled"

delete = Button(window, text="Delete Category", command=deleteCategory, bg="red", fg="white")
delete.grid(row=5, columnspan=2, sticky=W+E)
delete["state"] = "disabled"

mostrarCategorias()

window.mainloop()
