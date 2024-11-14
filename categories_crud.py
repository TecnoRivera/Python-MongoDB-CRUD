import pymongo
from tkinter import *
from tkinter import messagebox, ttk
from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000
URI = f"mongodb://{HOST}:{PORT}/"
BD = "blog"
COLLECTION_CATEGORIES = "categories"
COLLECTION_ARTICLES = "articles"
COLLECTION_ARTICLE_CATEGORIES = "article_categories"
COLLECTION_USERS = "users"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
categories_collection = database[COLLECTION_CATEGORIES]
articles_collection = database[COLLECTION_ARTICLES]
article_categories_collection = database[COLLECTION_ARTICLE_CATEGORIES]
users_collection = database[COLLECTION_USERS]

def addCategory(category_name, category_url, user_email):
    user = users_collection.find_one({"email": user_email})
    if not user:
        messagebox.showerror("Error", "El usuario no está registrado. No se puede agregar una categoría.")
        return

    if category_name:
        try:
            category = {"name": category_name, "url": category_url, "user_id": user["_id"]}
            result = categories_collection.insert_one(category)
            print("Categoría agregada con éxito.")
        except pymongo.errors.ConnectionFailure as err:
            print("Error:", err)
    else:
        messagebox.showerror("Error", "El campo 'Category Name' no puede estar vacío.")

def addCategoryToArticle(article_id, category_id):
    try:
        article_id_obj = ObjectId(article_id)
        category_id_obj = ObjectId(category_id)
        relationship = {
            "article_id": article_id_obj,
            "category_id": category_id_obj
        }
        article_categories_collection.insert_one(relationship)
        print("Categoría asociada al artículo con éxito.")
    except pymongo.errors.ConnectionFailure as err:
        print("Error:", err)

def deleteCategory(category_id, table):
    try:
        result = categories_collection.delete_one({"_id": ObjectId(category_id)})
        if result.deleted_count > 0:
            messagebox.showinfo("Eliminado", "Categoría eliminada con éxito.")
            displayCategories(table)
        else:
            messagebox.showerror("Error", "No se pudo eliminar la categoría.")
    except pymongo.errors.ConnectionFailure as err:
        print("Error al eliminar la categoría:", err)

def editCategory(category_id, new_name, new_url, table):
    try:
        result = categories_collection.update_one(
            {"_id": ObjectId(category_id)},
            {"$set": {"name": new_name, "url": new_url}}
        )
        if result.modified_count > 0:
            messagebox.showinfo("Editado", "Categoría editada con éxito.")
            displayCategories(table)
        else:
            messagebox.showerror("Error", "No se pudo editar la categoría.")
    except pymongo.errors.ConnectionFailure as err:
        print("Error al editar la categoría:", err)

def displayCategories(table):
    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        
        documents = categories_collection.find()
        for document in documents:
            category_name = document.get("name", "No name")
            category_url = document.get("url", "No URL")
            table.insert('', 'end', text=document["_id"], values=(category_name, category_url))
    except pymongo.errors.ConnectionFailure as err:
        print("Error al obtener categorías:", err)

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

def createCategoryInterface(window):

    Label(window, text="Category Name").grid(row=0, column=0, padx=10, pady=5)
    category_name = Entry(window)
    category_name.grid(row=0, column=1, padx=10, pady=5)

    Label(window, text="Category URL").grid(row=1, column=0, padx=10, pady=5)
    category_url = Entry(window)
    category_url.grid(row=1, column=1, padx=10, pady=5)

    Label(window, text="Your Email").grid(row=2, column=0, padx=10, pady=5)
    user_email = Entry(window)
    user_email.grid(row=2, column=1, padx=10, pady=5)

    create_button = Button(window, text="Add Category", command=lambda: addCategory(category_name.get(), category_url.get(), user_email.get()), bg="green", fg="white")
    create_button.grid(row=3, columnspan=2, pady=10)

    table = ttk.Treeview(window, columns=("name", "url"))
    table.grid(row=4, column=0, columnspan=2, padx=10, pady=10)
    table.heading("#0", text="ID")
    table.heading("name", text="Category Name")
    table.heading("url", text="Category URL")
    table.column("#0", width=100, stretch=False)
    table.column("name", width=200, stretch=True)
    table.column("url", width=200, stretch=True)
    
    displayCategories(table)

    def on_delete():
        selected_item = table.selection()
        if selected_item:
            category_id = table.item(selected_item)["text"]
            deleteCategory(category_id, table)

    def on_edit():
        selected_item = table.selection()
        if selected_item:
            category_id = table.item(selected_item)["text"]
            new_name = category_name.get()
            new_url = category_url.get()
            if new_name and new_url:
                editCategory(category_id, new_name, new_url, table)
            else:
                messagebox.showerror("Error", "Los campos 'Category Name' y 'Category URL' no pueden estar vacíos.")

    delete_button = Button(window, text="Delete Category", command=on_delete, bg="red", fg="white")
    delete_button.grid(row=5, column=0, pady=10)

    edit_button = Button(window, text="Edit Category", command=on_edit, bg="blue", fg="white")
    edit_button.grid(row=5, column=1, pady=10)

    Label(window, text="Assign Category to Article").grid(row=6, column=0, padx=10, pady=5)
    
    article_table = ttk.Treeview(window, columns=("title"))
    article_table.grid(row=7, column=0, columnspan=2, padx=10, pady=10)
    article_table.heading("#0", text="ID")
    article_table.heading("title", text="Article Title")
    article_table.column("#0", width=100, stretch=False)
    article_table.column("title", width=200, stretch=True)

    displayArticles(article_table)

    def on_article_select(event):
        selected_article_id = article_table.item(article_table.selection())["text"]
        selected_category_id = table.item(table.selection())["text"]
        addCategoryToArticle(selected_article_id, selected_category_id)

    article_table.bind("<Double-1>", on_article_select)

window = Tk()
window.title("Gestión de Categorías")
createCategoryInterface(window)
window.mainloop()
