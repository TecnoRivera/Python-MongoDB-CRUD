import pymongo
from tkinter import *
from tkinter import messagebox, ttk

from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000
URI = f"mongodb://{HOST}:{PORT}/"
BD = "blog"
COLLECTION = "categories"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
collection = database[COLLECTION]

def addCategory(category_name, category_url):
    if category_name:
        try:
            category = {"name": category_name, "url": category_url}
            result = collection.insert_one(category)
            print("Categoría agregada con éxito.")
        except pymongo.errors.ConnectionFailure as err:
            print("Error:", err)
    else:
        messagebox.showerror("Error", "El campo 'Category Name' no puede estar vacío")

def displayCategories(table):

    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        
        documents = collection.find()
        for document in documents:
            category_name = document.get("name", "No name")
            category_url = document.get("url", "No URL")
            table.insert('', 'end', text=document["_id"], values=(category_name, category_url))
    except pymongo.errors.ConnectionFailure as err:
        print("Error al obtener categorías:", err)

def createCategoryInterface(window):

    Label(window, text="Category Name").grid(row=0, column=0, padx=10, pady=5)
    category_name = Entry(window)
    category_name.grid(row=0, column=1, padx=10, pady=5)

    Label(window, text="Category URL").grid(row=1, column=0, padx=10, pady=5)
    category_url = Entry(window)
    category_url.grid(row=1, column=1, padx=10, pady=5)

    create_button = Button(window, text="Add Category", command=lambda: addCategory(category_name.get(), category_url.get()), bg="green", fg="white")
    create_button.grid(row=2, columnspan=2, pady=10)

    table = ttk.Treeview(window, columns=("name", "url"))
    table.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    table.heading("#0", text="ID") 
    table.heading("name", text="Category Name")  
    table.heading("url", text="Category URL") 
    table.column("#0", width=100, stretch=False)  
    table.column("name", width=200, stretch=True)  
    table.column("url", width=200, stretch=True)  

    displayCategories(table)

window = Tk()
window.title("Gestión de Categorías")
createCategoryInterface(window)
window.mainloop()
