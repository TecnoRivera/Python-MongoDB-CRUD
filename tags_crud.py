import pymongo
from tkinter import *
from tkinter import messagebox, ttk
from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000
URI = f"mongodb://{HOST}:{PORT}/"
BD = "blog"
COLLECTION = "tags"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
collection = database[COLLECTION]

def addTag(tag_Name, tag_Url):

    if tag_Name and tag_Url:
        try:
            tag = {"name": tag_Name, "url": tag_Url}
            result = collection.insert_one(tag)
            print("Tag agregado con éxito.")
        except pymongo.errors.ConnectionFailure as err:
            print("Error:", err)
    else:
        messagebox.showerror("Error", "El campo 'Tag Name' y 'Tag URL' no pueden estar vacíos")

def displayTags(table):

    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        
        documents = collection.find()
        for document in documents:
            tag_Name = document.get("name", "No name")
            tag_Url = document.get("url", "No URL")
            table.insert('', 'end', text=document["_id"], values=(tag_Name, tag_Url))
    except pymongo.errors.ConnectionFailure as err:
        print("Error al obtener tags:", err)

def createTagInterface(window):

    Label(window, text="Tag Name").grid(row=0, column=0, padx=10, pady=5)
    tag_name = Entry(window)
    tag_name.grid(row=0, column=1, padx=10, pady=5)

    Label(window, text="Tag URL").grid(row=1, column=0, padx=10, pady=5)
    tag_url = Entry(window)
    tag_url.grid(row=1, column=1, padx=10, pady=5)

    create_button = Button(window, text="Add Tag", command=lambda: addTag(tag_name.get(), tag_url.get()), bg="green", fg="white")
    create_button.grid(row=2, columnspan=2, pady=10)

    table = ttk.Treeview(window, columns=("name", "url"))
    table.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    table.heading("#0", text="ID") 
    table.heading("name", text="Tag Name")  
    table.heading("url", text="Tag URL")  
    table.column("#0", width=100, stretch=False)  
    table.column("name", width=200, stretch=True)  
    table.column("url", width=300, stretch=True)  

    displayTags(table)

window = Tk()
window.title("Gestión de Tags")
createTagInterface(window)
window.mainloop()
