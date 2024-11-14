import pymongo
from tkinter import *
from tkinter import messagebox, ttk
from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000
URI = f"mongodb://{HOST}:{PORT}/"
BD = "blog"
COLLECTION_TAGS = "tags"
COLLECTION_ARTICLES = "articles"
COLLECTION_ARTICLE_TAGS = "article_tags"
COLLECTION_USERS = "users"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
tags_collection = database[COLLECTION_TAGS]
articles_collection = database[COLLECTION_ARTICLES]
article_tags_collection = database[COLLECTION_ARTICLE_TAGS]
users_collection = database[COLLECTION_USERS]

def addTag(tag_Name, tag_Url, user_email):
    user = users_collection.find_one({"email": user_email})
    if not user:
        messagebox.showerror("Error", "El usuario no está registrado. No se puede agregar un tag.")
        return

    if tag_Name and tag_Url:
        try:
            tag = {"name": tag_Name, "url": tag_Url, "user_id": user["_id"]}
            result = tags_collection.insert_one(tag)
            print("Tag agregado con éxito.")
        except pymongo.errors.ConnectionFailure as err:
            print("Error:", err)
    else:
        messagebox.showerror("Error", "Los campos 'Tag Name' y 'Tag URL' no pueden estar vacíos")

def addTagToArticle(article_id, tag_id):
    try:
        article_id_obj = ObjectId(article_id)
        tag_id_obj = ObjectId(tag_id)
        relationship = {
            "article_id": article_id_obj,
            "tag_id": tag_id_obj
        }
        article_tags_collection.insert_one(relationship)
        print("Tag asociado al artículo con éxito.")
    except pymongo.errors.ConnectionFailure as err:
        print("Error:", err)

def deleteTag(tag_id, table):
    try:
        result = tags_collection.delete_one({"_id": ObjectId(tag_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("Eliminado", "Tag eliminado con éxito.")
            displayTags(table)
        else:
            messagebox.showerror("Error", "No se pudo eliminar el tag.")
    except pymongo.errors.ConnectionFailure as err:
        print("Error al eliminar el tag:", err)

def editTag(tag_id, new_name, new_url, table):
    try:
        result = tags_collection.update_one(
            {"_id": ObjectId(tag_id)},
            {"$set": {"name": new_name, "url": new_url}}
        )
        if result.modified_count > 0:
            messagebox.showinfo("Editado", "Tag editado con éxito.")
            displayTags(table)
        else:
            messagebox.showerror("Error", "No se pudo editar el tag.")
    except pymongo.errors.ConnectionFailure as err:
        print("Error al editar el tag:", err)

def displayTags(table):
    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        
        documents = tags_collection.find()
        for document in documents:
            tag_Name = document.get("name", "No name")
            tag_Url = document.get("url", "No URL")
            table.insert('', 'end', text=document["_id"], values=(tag_Name, tag_Url))
    except pymongo.errors.ConnectionFailure as err:
        print("Error al obtener tags:", err)

def displayArticles(table):
    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        
        documents = articles_collection.find()
        for document in documents:
            article_title = document.get("title", "No title")
            table.insert('', 'end', text=document["_id"], values=(article_title,))
    except pymongo.errors.ConnectionFailure as err:
        print("Error al obtener artículos:", err)

def createTagInterface(window):

    Label(window, text="Tag Name").grid(row=0, column=0, padx=10, pady=5)
    tag_name = Entry(window)
    tag_name.grid(row=0, column=1, padx=10, pady=5)

    Label(window, text="Tag URL").grid(row=1, column=0, padx=10, pady=5)
    tag_url = Entry(window)
    tag_url.grid(row=1, column=1, padx=10, pady=5)

    Label(window, text="Your Email").grid(row=2, column=0, padx=10, pady=5)
    user_email = Entry(window)
    user_email.grid(row=2, column=1, padx=10, pady=5)

    create_button = Button(window, text="Add Tag", command=lambda: addTag(tag_name.get(), tag_url.get(), user_email.get()), bg="green", fg="white")
    create_button.grid(row=3, columnspan=2, pady=10)

    table = ttk.Treeview(window, columns=("name", "url"))
    table.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    table.heading("#0", text="ID")
    table.heading("name", text="Tag Name")
    table.heading("url", text="Tag URL")
    table.column("#0", width=100, stretch=False)
    table.column("name", width=200, stretch=True)
    table.column("url", width=300, stretch=True)
    
    displayTags(table)

    def on_delete():
        selected_item = table.selection()
        if selected_item:
            tag_id = table.item(selected_item)["text"]
            deleteTag(tag_id, table)

    def on_edit():
        selected_item = table.selection()
        if selected_item:
            tag_id = table.item(selected_item)["text"]
            new_name = tag_name.get()
            new_url = tag_url.get()
            if new_name and new_url:
                editTag(tag_id, new_name, new_url, table)
            else:
                messagebox.showerror("Error", "Los campos 'Tag Name' y 'Tag URL' no pueden estar vacíos.")

    delete_button = Button(window, text="Delete Tag", command=on_delete, bg="red", fg="white")
    delete_button.grid(row=5, column=0, pady=10)

    edit_button = Button(window, text="Edit Tag", command=on_edit, bg="blue", fg="white")
    edit_button.grid(row=5, column=1, pady=10)

    Label(window, text="Assign Tag to Article").grid(row=6, column=0, padx=10, pady=5)
    
    article_table = ttk.Treeview(window, columns=("title"))
    article_table.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    article_table.heading("#0", text="ID")
    article_table.heading("title", text="Article Title")
    article_table.column("#0", width=100, stretch=False)
    article_table.column("title", width=200, stretch=True)

    displayArticles(article_table)

    def on_article_select(event):
        selected_article_id = article_table.item(article_table.selection())["text"]
        selected_tag_id = table.item(table.selection())["text"]
        addTagToArticle(selected_article_id, selected_tag_id)

    article_table.bind("<Double-1>", on_article_select)

window = Tk()
window.title("Gestión de Tags")
createTagInterface(window)
window.mainloop()
