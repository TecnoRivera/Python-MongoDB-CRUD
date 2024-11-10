# article_crud.py
from tkinter import *
from tkinter import messagebox, ttk
import pymongo
from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000

URI = "mongodb://" + HOST + ":" + PORT + "/"

BD = "blog"
COLLECTION = "articles"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
collection = database[COLLECTION]

def mostrarDatos():
    try:
        for document in collection.find():
            table.insert('', 0, text=document["_id"], values=(document["title"], document["date"], document["text"]))
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Time exceed", err)
    except pymongo.errors.ConnectionFailure as err:
        print("Fail trying to connect to Mongodb", err)

def addArticle():
    if len(title.get()) != 0 and len(date.get()) != 0 and len(text.get()) != 0:
        try:
            document = {"title": title.get(), "date": date.get(), "text": text.get()}
            collection.insert_one(document)
        except pymongo.errors.ConnectionFailure as err:
            print(err)
    mostrarDatos()

def editArticle():
    global ID_ARTICLE
    if len(title.get()) != 0 and len(date.get()) != 0 and len(text.get()) != 0:
        try:
            idSearch = {"_id": ObjectId(ID_ARTICLE)}
            newValues = {"$set": {"title": title.get(), "date": date.get(), "text": text.get()}}
            collection.update_one(idSearch, newValues)
            title.delete(0, END)
            date.delete(0, END)
            text.delete(0, END)
        except pymongo.errors.ConnectionFailure as err:
            print(err)
    mostrarDatos()

def deleteArticle():
    global ID_ARTICLE
    try:
        idSearch = {"_id": ObjectId(ID_ARTICLE)}
        collection.delete_one(idSearch)
    except pymongo.errors.ConnectionFailure as err:
        print(err)
    mostrarDatos()

def doubleClickTable(event):
    global ID_ARTICLE
    ID_ARTICLE = str(table.item(table.selection())["text"])
    document = collection.find({"_id": ObjectId(ID_ARTICLE)})[0]
    title.delete(0, END)
    title.insert(0, document["title"])
    date.delete(0, END)
    date.insert(0, document["date"])
    text.delete(0, END)
    text.insert(0, document["text"])
    create["state"] = "disabled"
    edit["state"] = "normal"
    delete["state"] = "normal"

window = Tk()
table = ttk.Treeview(window, columns=("title", "date", "text"))
table.grid(row=0, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("title", text="Title")
table.heading("date", text="Date")
table.heading("text", text="Text")
table.bind("<Double-1>", doubleClickTable)

Label(window, text="Title").grid(row=1, column=0)
title = Entry(window)
title.grid(row=1, column=1, sticky=W+E)

Label(window, text="Date").grid(row=2, column=0)
date = Entry(window)
date.grid(row=2, column=1, sticky=W+E)

Label(window, text="Text").grid(row=3, column=0)
text = Entry(window)
text.grid(row=3, column=1, sticky=W+E)

create = Button(window, text="Add Article", command=addArticle, bg="green")
create.grid(row=4, columnspan=2, sticky=W+E)

edit = Button(window, text="Edit Article", command=editArticle, bg="yellow")
edit.grid(row=5, columnspan=2, sticky=W+E)
edit["state"] = "disabled"

delete = Button(window, text="Delete Article", command=deleteArticle, bg="red", fg="white")
delete.grid(row=6, columnspan=2, sticky=W+E)
delete["state"] = "disabled"

mostrarDatos()

window.mainloop()