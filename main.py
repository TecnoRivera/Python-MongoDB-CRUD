from tkinter import *
import subprocess

def open_users_crud():
    subprocess.Popen(["python", "user_crud.py"])

def open_articles_crud():
    
    subprocess.Popen(["python", "new_article.py"])

def open_comments_crud():
    subprocess.Popen(["python", "comments_crud.py"])

def open_categories_crud():
    subprocess.Popen(["python", "categories_crud.py"])

def open_tags_crud():
    subprocess.Popen(["python", "tags_crud.py"])

window = Tk()
window.title("Main Menu")

window_width = 500
window_height = 400

screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2

window.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

window.config(bg="#333333")  

button_font = ("Arial", 12, "bold")
button_bg = "#4CAF50"      
button_fg = "white"

Button(window, text="Users CRUD", command=open_users_crud, font=button_font, bg=button_bg, fg=button_fg).pack(fill=X, pady=10, padx=20)
Button(window, text="Articles CRUD", command=open_articles_crud, font=button_font, bg=button_bg, fg=button_fg).pack(fill=X, pady=10, padx=20)
Button(window, text="Comments CRUD", command=open_comments_crud, font=button_font, bg=button_bg, fg=button_fg).pack(fill=X, pady=10, padx=20)
Button(window, text="Categories CRUD", command=open_categories_crud, font=button_font, bg=button_bg, fg=button_fg).pack(fill=X, pady=10, padx=20)
Button(window, text="Tags CRUD", command=open_tags_crud, font=button_font, bg=button_bg, fg=button_fg).pack(fill=X, pady=10, padx=20)

window.mainloop()