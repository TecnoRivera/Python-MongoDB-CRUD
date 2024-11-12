#comments_crud.py
import pymongo
from tkinter import *
from tkinter import messagebox, ttk
from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000
URI = f"mongodb://{HOST}:{PORT}/"
BD = "blog"
COLLECTION = "comments"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
collection = database[COLLECTION]

def addComment(comment_name, comment_url, article_id):
    """Agrega un comentario con nombre, URL y ID de artículo."""
    if comment_name and comment_url:
        try:
            comment = {
                "name": comment_name,
                "url": comment_url,
                "article_id": ObjectId(article_id)
            }
            collection.insert_one(comment)
            print("Comentario agregado con éxito.")
        except pymongo.errors.ConnectionFailure as err:
            print("Error al conectar a MongoDB:", err)
    else:
        messagebox.showerror("Error", "Los campos 'Name' y 'URL' no pueden estar vacíos.")

def displayComments(table, article_id):
    """Muestra los comentarios en la tabla vinculados a un artículo específico."""
    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)

        documents = collection.find({"article_id": ObjectId(article_id)})
        for document in documents:
            comment_name = document.get("name", "No name")
            comment_url = document.get("url", "No URL")
            table.insert('', 'end', text=document["_id"], values=(comment_name, comment_url))
    except pymongo.errors.ConnectionFailure as err:
        print("Error al obtener comentarios:", err)

def createCommentInterface(window, article_id):
    """Crea la interfaz gráfica para gestionar comentarios."""
    Label(window, text="Comment Name").grid(row=0, column=0, padx=10, pady=5)
    comment_name = Entry(window)
    comment_name.grid(row=0, column=1, padx=10, pady=5)

    Label(window, text="Comment URL").grid(row=1, column=0, padx=10, pady=5)
    comment_url = Entry(window)
    comment_url.grid(row=1, column=1, padx=10, pady=5)

    create_button = Button(window, text="Add Comment", command=lambda: addComment(comment_name.get(), comment_url.get(), article_id), bg="green", fg="white")
    create_button.grid(row=2, columnspan=2, pady=10)

    table = ttk.Treeview(window, columns=("name", "url"))
    table.grid(row=3, column=0, columnspan=2, padx=10, pady=10)
    table.heading("#0", text="ID") 
    table.heading("name", text="Comment Name")  
    table.heading("url", text="Comment URL") 
    table.column("#0", width=100, stretch=False)  
    table.column("name", width=200, stretch=True)  
    table.column("url", width=200, stretch=True)  

    displayComments(table, article_id)

window = Tk()
window.title("Gestión de Comentarios")
createCommentInterface(window, "some_article_id")  
window.mainloop()
