# article_crud.py
from tkinter import *
from tkinter import messagebox, ttk
import tkinter as tk
import pymongo
import user_posts
from bson.objectid import ObjectId

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000

URI = "mongodb://" + HOST + ":" + PORT + "/"

BD = "blog"
collection_find = "articles"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
collection = database[collection_find]

users_list = []
users_list_id = []

def on_press_user_button():
    selected_user = combo.get()

    if selected_user and selected_user.strip():
        """ email_key_map = dict(zip(users_list, users_list_id))
        user = email_key_map.get(selected_user, "Email not found") """
        user_posts.show_user_posts(selected_user)

def fill_combo_options():
    try:
        users_list = []
        users_list_id = []
        collection_find = "users";
        collection = database[collection_find]

        for document in collection.find():
            if "email" in document:
                users_list_id.append(document["_id"])
                users_list.append(document["email"])
            
            print(document)
    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Time exceed", err)
    except pymongo.errors.ConnectionFailure as err:
        print("Fail trying to connect to Mongodb", err)

    return ttk.Combobox(state="readonly", values=users_list_id)


main_window = tk.Tk()
main_window.config(width=300, height=200)
main_window.title("Combobox")
combo = fill_combo_options()
combo.place(x=50, y=50)

button_acc = ttk.Button(text= "Aceptar Usuario", command=on_press_user_button)
button_acc.place(x=50, y=100)

main_window.mainloop()