from tkinter import *
import subprocess

def open_users_crud():
    subprocess.Popen(["python", "user_crud.py"])

def open_articles_crud():
    subprocess.Popen(["python", "article_crud.py"])

def open_comments_crud():
    subprocess.Popen(["python", "comments_crud.py"])

def open_categories_crud():
    subprocess.Popen(["python", "categories_crud.py"])

def open_tags_crud():
    subprocess.Popen(["python", "tags_crud.py"])

window = Tk()
window.title("Main Menu")

Button(window, text="Users CRUD", command=open_users_crud).pack(fill=X)
Button(window, text="Articles CRUD", command=open_articles_crud).pack(fill=X)
Button(window, text="Comments CRUD", command=open_comments_crud).pack(fill=X)
Button(window, text="Categories CRUD", command=open_categories_crud).pack(fill=X)
Button(window, text="Tags CRUD", command=open_tags_crud).pack(fill=X)

window.mainloop()