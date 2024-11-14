# article_crud.py
from tkinter import *
from tkinter import messagebox, ttk
import pymongo
import comments_crud
import tags_crud
import categories_crud
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

current_user = None
ui_table = None
title = None
date = None
text = None
create = None
edit = None
delete = None
comments = None
tags = None
categories = None

def mostrarDatos():
    for item in ui_table.get_children():
        ui_table.delete(item)

    try:
        for document in collection.find({"belongs_to": current_user}):
            ui_table.insert('', 0, text=document["_id"], values=(document["title"], document["date"], document["text"]))
            pass
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Time exceed", err)
    except pymongo.errors.ConnectionFailure as err:
        print("Fail trying to connect to Mongodb", err)


def create_window():
    global ui_table, title, date, text, create, edit, delete, comments, tags, categories

    window = Tk()
    ui_table = ttk.Treeview(window, columns=("title", "date", "text"))
    ui_table.grid(row=0, column=0, columnspan=2)
    ui_table.heading("#0", text="ID")
    ui_table.heading("title", text="Title")
    ui_table.heading("date", text="Date")
    ui_table.heading("text", text="Text")
    ui_table.bind("<Double-1>", doubleClickTable)

    Label(window, text="Title").grid(row=1, column=0)
    title = Entry(window)
    title.grid(row=1, column=1, sticky=W+E)

    Label(window, text="Date").grid(row=2, column=0)
    date = Entry(window)
    date.grid(row=2, column=1, sticky=W+E)

    Label(window, text="Text").grid(row=3, column=0)
    text = Entry(window)
    text.grid(row=3, column=1, sticky=W+E)

    comments = Button(window, text="Comments", command=check_comments, bg="#673AB7", fg="white")
    comments.grid(row=4, column=0, columnspan=1, sticky=W+E)
    comments["state"] = "disabled"

    create = Button(window, text="Add Article", command=addArticle, bg="green")
    create.grid(row=4, column=1, columnspan=2, sticky=W+E)

    tags = Button(window, text="Tags", command=check_tags, bg="#673AB7", fg="white")
    tags.grid(row=5, column=0, columnspan=1, sticky=W+E)
    tags["state"] = "disabled"

    edit = Button(window, text="Edit Article", command=editArticle, bg="yellow")
    edit.grid(row=5, column=1, columnspan=2, sticky=W+E)
    edit["state"] = "disabled"

    categories = Button(window, text="Categories", command=check_categories, bg="#673AB7", fg="white")
    categories.grid(row=6, column=0, columnspan=1, sticky=W+E)
    categories["state"] = "disabled"

    delete = Button(window, text="Delete Article", command=deleteArticle, bg="red", fg="white")
    delete.grid(row=6, column=1, columnspan=2, sticky=W+E)
    delete["state"] = "disabled"
    
    mostrarDatos()

    window.mainloop()


def show_user_posts(selected_id):
    global current_user

    current_user = selected_id
    print(f"Showing posts for user ID: {current_user}")

    create_window();


def addArticle():
    if len(title.get()) != 0 and len(date.get()) != 0 and len(text.get()) != 0:
        try:
            document = {"title": title.get(), "date": date.get(), "text": text.get(), "belongs_to": current_user}
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


def check_comments():
    print(ID_ARTICLE)
    comments_crud.show_article_comments(ID_ARTICLE)

def check_tags():
    print(ID_ARTICLE)
    tags_crud.show_article_tags(ID_ARTICLE)

def check_categories():
    print(ID_ARTICLE)
    categories_crud.show_article_categories(ID_ARTICLE)

def doubleClickTable(event):
    global ID_ARTICLE
    ID_ARTICLE = str(ui_table.item(ui_table.selection())["text"])
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
    comments["state"] = "normal"
    tags["state"] = "normal"
    categories["state"] = "normal"



