import pymongo
from tkinter import *
from tkinter import messagebox, ttk
from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000
URI = f"mongodb://{HOST}:{PORT}/"

BD = "blog"
COLLECTION_COMMENTS = "comments"
COLLECTION_USERS = "users" 

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
comments_collection = database[COLLECTION_COMMENTS]
users_collection = database[COLLECTION_USERS]


article_id = None

current_article = None
ui_table = None
title = None
date = None
text = None
create = None
edit = None
delete = None



def create_window():
    window = Tk()
    window.title("Gestión de Comentarios")

    article = comments_collection.find_one()
    if article:
        article_id = str(article["_id"])
    else:
        article_id = str(ObjectId())

    createCommentInterface(window, article_id)
    window.mainloop()


def show_article_comments(selected_id):
    global current_article

    current_article = selected_id
    print(f"Showing comments for article: {current_article}")

    create_window();



def addComment(comment_name, comment_url, article_id, user_email):
    user = users_collection.find_one({"email": user_email})
    if not user:
        messagebox.showerror("Error", "El usuario no está registrado. No se puede agregar un comentario.")
        return

    if comment_name and comment_url:
        try:
            try:
                article_id_obj = ObjectId(article_id)
            except Exception as e:
                messagebox.showerror("Error", "ID de artículo no válido.")
                return
            
            comment = {
                "name": comment_name,
                "url": comment_url,
                "article_id": article_id_obj,
                "user_id": user["_id"], 
                "belongs_to": current_article
            }
            comments_collection.insert_one(comment)
            print("Comentario agregado con éxito.")
        except pymongo.errors.ConnectionFailure as err:
            print("Error al conectar a MongoDB:", err)
    else:
        messagebox.showerror("Error", "Los campos 'Name' y 'URL' no pueden estar vacíos.")

def deleteComment(comment_id):
    try:
        comment_id_obj = ObjectId(comment_id)
        comments_collection.delete_one({"_id": comment_id_obj})
        print("Comentario eliminado con éxito.")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo eliminar el comentario: {e}")
    displayComments(table, article_id)

def editComment(comment_id, comment_name, comment_url):
    try:
        comment_id_obj = ObjectId(comment_id)
        updated_comment = {
            "$set": {
                "name": comment_name,
                "url": comment_url
            }
        }
        comments_collection.update_one({"_id": comment_id_obj}, updated_comment)
        print("Comentario actualizado con éxito.")
        displayComments(table, article_id)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo editar el comentario: {e}")



def displayComments(table, article_id):
    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)

        try:
            article_id_obj = ObjectId(article_id)
        except Exception as e:
            messagebox.showerror("Error", "ID de artículo no válido.")
            return

        documents = comments_collection.find({"belongs_to": current_article})
        for document in documents:
            comment_name = document.get("name", "No name")
            comment_url = document.get("url", "No URL")
            table.insert('', 'end', text=document["_id"], values=(comment_name, comment_url))
    except pymongo.errors.ConnectionFailure as err:
        print("Error al obtener comentarios:", err)

def on_comment_select(event):
    global selected_comment_id
    selected_comment_id = table.item(table.selection())["text"]
    selected_comment_name = table.item(table.selection())["values"][0]
    selected_comment_url = table.item(table.selection())["values"][1]
    
    comment_name.delete(0, END)
    comment_name.insert(0, selected_comment_name)
    comment_url.delete(0, END)
    comment_url.insert(0, selected_comment_url)

def createCommentInterface(window, article_id):
    global comment_name, comment_url, table

    Label(window, text="Comment Name").grid(row=0, column=0, padx=10, pady=5)
    comment_name = Entry(window)
    comment_name.grid(row=0, column=1, padx=10, pady=5)

    Label(window, text="Comment URL").grid(row=1, column=0, padx=10, pady=5)
    comment_url = Entry(window)
    comment_url.grid(row=1, column=1, padx=10, pady=5)

    Label(window, text="Your Email").grid(row=2, column=0, padx=10, pady=5)
    user_email = Entry(window)
    user_email.grid(row=2, column=1, padx=10, pady=5)

    create_button = Button(window, text="Add Comment", command=lambda: addComment(comment_name.get(), comment_url.get(), article_id, user_email.get()), bg="green", fg="white")
    create_button.grid(row=3, columnspan=2, pady=10)

    edit_button = Button(window, text="Edit Comment", command=lambda: editComment(selected_comment_id, comment_name.get(), comment_url.get()), bg="yellow")
    edit_button.grid(row=4, columnspan=2, pady=5)

    delete_button = Button(window, text="Delete Comment", command=lambda: deleteComment(selected_comment_id), bg="red", fg="white")
    delete_button.grid(row=5, columnspan=2, pady=5)

    table = ttk.Treeview(window, columns=("name", "url"))
    table.grid(row=6, column=0, columnspan=2, padx=10, pady=10)
    table.heading("#0", text="ID")
    table.heading("name", text="Comment Name")
    table.heading("url", text="Comment URL")
    table.column("#0", width=100, stretch=False)
    table.column("name", width=200, stretch=True)
    table.column("url", width=200, stretch=True)
    
    table.bind("<Double-1>", on_comment_select) 

    displayComments(table, article_id)


