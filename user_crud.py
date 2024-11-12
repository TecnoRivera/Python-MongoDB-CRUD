# user_crud.py
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pymongo
from bson.objectid import ObjectId
import pymongo.errors

HOST = "localhost"
PORT = "27017"
TIMEOUT = 1000

URI = f"mongodb://{HOST}:{PORT}/"
BD = "blog"
COLLECTION = "users"

client = pymongo.MongoClient(URI, serverSelectionTimeoutMS=TIMEOUT)
database = client[BD]
collection = database[COLLECTION]

selected_user_id = None

def mostrarDatos(name="", email=""):
    objectSearch = {}
    if name:
        objectSearch["name"] = name
    if email:
        objectSearch["email"] = email

    try:
        registers = table.get_children()
        for register in registers:
            table.delete(register)
        documents = collection.find(objectSearch) if objectSearch else collection.find()
        for document in documents:
            table.insert('', 'end', text=document["_id"], values=(document["name"], document["email"]))

    except pymongo.errors.ServerSelectionTimeoutError as err:
        print("Tiempo excedido:", err)
    except pymongo.errors.ConnectionFailure as err:
        print("Error al intentar conectar con MongoDB:", err)



def addUser():
    if name.get() and email.get():
        try:
            document = {"name": name.get(), "email": email.get()}
            collection.insert_one(document)
            name.delete(0, END)
            email.delete(0, END)
        except pymongo.errors.ConnectionFailure as err:
            print("Error:", err)
    else:
        messagebox.showerror("Error", "Los campos no pueden estar vacíos")
    mostrarDatos()



def editRegister():
    global selected_user_id
    if name.get() and email.get():
        try:
            idSearch = {"_id": ObjectId(selected_user_id)}
            newValues = {"$set": {"name": name.get(), "email": email.get()}}
            result = collection.update_one(idSearch, newValues)

            name.delete(0, END)
            email.delete(0, END)
        except pymongo.errors.ConnectionFailure as err:
            print("Error:", err)
    else:
        messagebox.showerror("Error", "Los campos no pueden estar vacíos")
    mostrarDatos()


def deleteRegister():
    global selected_user_id
    try:
        idSearch = {"_id": ObjectId(selected_user_id)}
        result = collection.delete_one(idSearch)

        name.delete(0, END)
        email.delete(0, END)
    except pymongo.errors.ConnectionFailure as err:
        print("Error:", err)

    mostrarDatos()

def doubleClickTable(event):
    global selected_user_id
    selected_user_id = str(table.item(table.selection())["text"])
    document = collection.find_one({"_id": ObjectId(selected_user_id)})
    if document:
        name.delete(0, END)
        name.insert(0, document["name"])
        email.delete(0, END)
        email.insert(0, document["email"])
        create["state"] = "disabled"
        edit["state"] = "normal"
        delete["state"] = "normal"
    else:
        print("No se encontró el documento con el ID:", selected_user_id)

window = Tk()
window.title("Gestión de Usuarios")

table = ttk.Treeview(window, columns=("name", "email"))
table.grid(row=1, column=0, columnspan=2)
table.heading("#0", text="ID")
table.heading("name", text="Name")
table.heading("email", text="Email")
table.bind("<Double-1>", doubleClickTable)

Label(window, text="Name").grid(row=2, column=0)
name = Entry(window)
name.grid(row=2, column=1, sticky=W+E)
name.focus()

Label(window, text="Email").grid(row=3, column=0)
email = Entry(window)
email.grid(row=3, column=1, sticky=W+E)

create = Button(window, text="Add User", command=addUser, bg="green", fg="white")
create.grid(row=5, columnspan=2, sticky=W+E)

edit = Button(window, text="Edit User", command=editRegister, bg="yellow")
edit.grid(row=6, columnspan=2, sticky=W+E)
edit["state"] = "disabled"

delete = Button(window, text="Delete User", command=deleteRegister, bg="red", fg="white")
delete.grid(row=7, columnspan=2, sticky=W+E)
delete["state"] = "disabled"

Label(window, text="Search for Name").grid(row=8, column=0)
searchName = Entry(window)
searchName.grid(row=8, column=1, sticky=W+E)

Label(window, text="Search for Email").grid(row=9, column=0)
searchEmail = Entry(window)
searchEmail.grid(row=9, column=1, sticky=W+E)

search = Button(window, text="Search User", command=lambda: mostrarDatos(searchName.get(), searchEmail.get()), bg="blue", fg="white")
search.grid(row=10, columnspan=2, sticky=W+E)

mostrarDatos()

def on_closing():
    client.close()
    window.destroy()

window.protocol("WM_DELETE_WINDOW", on_closing)
window.mainloop()
