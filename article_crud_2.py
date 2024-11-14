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

def mostrarDatos(title="", date="", text=""):
    objectSearch = {}
    if len(title) != 0:
        objectSearch["title"] = title
    if len(date) != 0:
        objectSearch["date"] = date
    if len(text) != 0:
        objectSearch["text"] = text
    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        for document in collection.find(objectSearch):
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
            title.delete(0, END)
            date.delete(0, END)
            text.delete(0, END)
        except pymongo.errors.ConnectionFailure as err:
            print(err)
    else:
        messagebox.showerror(message="Los campos no pueden estar vacios")
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
    else:
        messagebox.showerror("Los campos no pueden estar vacios")
    mostrarDatos()
    create["state"] = "normal"
    edit["state"] = "disabled"
    delete["state"] = "disabled"

def deleteArticle():
    global ID_ARTICLE
    try:
        idSearch = {"_id": ObjectId(ID_ARTICLE)}
        collection.delete_one(idSearch)
        title.delete(0, END)
        date.delete(0, END)
        text.delete(0, END)
    except pymongo.errors.ConnectionFailure as err:
        print(err)
    create["state"] = "normal"
    edit["state"] = "disabled"
    delete["state"] = "disabled"
    mostrarDatos()

def searchArticle():
    mostrarDatos(searchTitle.get(), searchDate.get(), searchText.get())

window = Tk()
table = ttk.Treeview(window, columns=("title", "date", "text"))
table.grid(row=1, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("#1", text="TITLE")
table.heading("#2", text="DATE")
table.heading("#3", text="TEXT")
table.bind("<Double-Button-1>", doubleClickTable)

def on_closing():
    client.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)

Label(window, text="Title").grid(row=2, column=0)
title = Entry(window)
title.grid(row=2, column=1, sticky=W+E)
title.focus()

Label(window, text="Date").grid(row=3, column=0)
date = Entry(window)
date.grid(row=3, column=1, sticky=W+E)

Label(window, text="Text").grid(row=4, column=0)
text = Entry(window)
text.grid(row=4, column=1, sticky=W+E)

create = Button(window, text="Add Article", command=addArticle, bg="green", fg="white")
create.grid(row=5, columnspan=2, sticky=W+E)

edit = Button(window, text="Edit Article", command=editArticle, bg="yellow")
edit.grid(row=6, columnspan=2, sticky=W+E)
edit["state"] = "disabled"

delete = Button(window, text="Delete Article", command=deleteArticle, bg="red", fg="white")
delete.grid(row=7, columnspan=2, sticky=W+E)
delete["state"] = "disabled"

Label(window, text="Search for title").grid(row=8, column=0)
searchTitle = Entry(window)
searchTitle.grid(row=8, column=1, sticky=W+E)

Label(window, text="Search for date").grid(row=9, column=0)
searchDate = Entry(window)
searchDate.grid(row=9, column=1, sticky=W+E)

Label(window, text="Search for text").grid(row=10, column=0)
searchText = Entry(window)
searchText.grid(row=10, column=1, sticky=W+E)

search = Button(window, text="Search article", command=searchArticle, bg="blue", fg="white")
search.grid(row=11, columnspan=2, sticky=W+E)

mostrarDatos()

window.mainloop()