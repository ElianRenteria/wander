import time
import customtkinter
from database import Database
from game import Game

db = Database()
def show(password_entry):
    current_show_state = password_entry.cget("show")
    if current_show_state == "*":
        password_entry.configure(show="")
    else:
        password_entry.configure(show="*")

def return_to_login_page(original_root, username, password, confirm_password, responseLabel):
    if username == "" or password == "" or confirm_password == "":
        responseLabel.configure(text="Please fill in all fields, and try again.", text_color="red")
        responseLabel.place(x=115, y=140)
    elif password != confirm_password:
        responseLabel.configure(text="Passwords do not match, please try again.", text_color="red")
        responseLabel.place(x=105, y=140)
    elif len(username) > 10:
        responseLabel.configure(text="Username is too long, please try again.", text_color="red")
        responseLabel.place(x=106, y=140)
    else:
        if db.check_user_exists(username):
            responseLabel.configure(text="User already exists, please try again.", text_color="red")
            responseLabel.place(x=115, y=140)
        else:
            db.create_user(username, password)
            responseLabel.configure(text="User created successfully!", text_color="green")
            responseLabel.place(x=155, y=140)
            original_root.update()
            time.sleep(1)
            original_root.destroy()
            login_page()
def signup_page(original_root):
    original_root.destroy()
    root = customtkinter.CTk()
    root.title("Wander")
    root.geometry("500x600")
    root.resizable(False, False)

    response = customtkinter.CTkLabel(root, text="Please enter your details", font=("Helvetica", 18))
    response.place(x=155, y=140)

    title = customtkinter.CTkLabel(root, text="Sign Up", font=("Helvetica", 48))
    title.place(x=167, y=70)

    username = customtkinter.CTkEntry(root, font=("Helvetica", 24), placeholder_text="Username", width=250)
    username.place(x=130, y=200)
    password = customtkinter.CTkEntry(root, font=("Helvetica", 24), placeholder_text="Password", show="*", width=250)
    password.place(x=130, y=250)
    confirm_password = customtkinter.CTkEntry(root, font=("Helvetica", 24), placeholder_text="Confirm Password", show="*", width=250)
    confirm_password.place(x=130, y=300)
    show_password = customtkinter.CTkButton(root, text="Show", font=("Helvetica", 10), width=10, height=40, command=lambda:show(password), fg_color=root["bg"], hover_color=root["bg"], text_color="red")
    show_password.place(x=385, y=246)
    show_password2 = customtkinter.CTkButton(root, text="Show", font=("Helvetica", 10), width=10, height=40,
                                            command=lambda: show(confirm_password), fg_color=root["bg"], hover_color=root["bg"],
                                            text_color="red")
    show_password2.place(x=385, y=296)

    register = customtkinter.CTkButton(root, text="Register", font=("Helvetica", 18), width=100, height=40, command=lambda:return_to_login_page(root, username.get(), password.get(), confirm_password.get(), response), fg_color="#71cc58", hover_color="#4e8c3c", text_color="black")
    register.place(x=200, y=380)

    login = customtkinter.CTkButton(root, text="Login", font=("Helvetica", 18), width=100, height=40, fg_color=root["bg"], hover_color=root["bg"], text_color="#5087c7")
    login.place(x=200, y=530)

    root.mainloop()

def login_Game(username, password, responseLabel, root):
    if username == "" or password == "":
        responseLabel.configure(text="Please fill in all fields, and try again.", text_color="red")
        responseLabel.place(x=115, y=150)
    elif db.check_password(username, password):
        responseLabel.configure(text="Login successful!", text_color="green")
        responseLabel.place(x=182, y=150)
        root.update()
        time.sleep(1)
        root.destroy()
        game = Game(db.get_user(username))
        game.run()
    else:
        responseLabel.configure(text="Invalid username or password, please try again.", text_color="red")
        responseLabel.place(x=65, y=150)

def login_page():
    root = customtkinter.CTk()
    root.title("Wander")
    root.geometry("500x600")
    root.resizable(False, False)

    response = customtkinter.CTkLabel(root, text="", font=("Helvetica", 18))
    response.place(x=155, y=140)

    title = customtkinter.CTkLabel(root, text="Wander", font=("Helvetica", 48))
    title.place(x=170, y=80)

    username = customtkinter.CTkEntry(root, font=("Helvetica", 24), placeholder_text="Username", width=250)
    username.place(x=130, y=200)
    password = customtkinter.CTkEntry(root, font=("Helvetica", 24), placeholder_text="Password", show="*", width=250)
    password.place(x=130, y=250)

    login = customtkinter.CTkButton(root, text="Login", font=("Helvetica", 18), width=100, height=40, command=lambda:login_Game(username.get(), password.get(), response, root))
    login.place(x=200, y=300)

    register = customtkinter.CTkButton(root, text="Register", font=("Helvetica", 18), width=100, height=40, fg_color=root["bg"], hover_color=root["bg"], text_color="lightgreen", command=lambda:signup_page(root))
    register.place(x=200, y=530)


    root.mainloop()


login_page()