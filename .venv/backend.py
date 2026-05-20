import bcrypt, admin_window, dbinfo
import customtkinter as ctk
from tkinter import *
from CTkListbox import CTkListbox

# laitta ohjelmalle systeemin 
ctk.set_appearance_mode("System") 

# luodaan ikkuna
root = ctk.CTk()
root.geometry("1000x600")
root.resizable(width=False, height=False)
root.title("Admin")

def get_input():
    try:
        # saadaan inputit
        username = username_input.get()
        password = password_input.get()     
        # tarkistaa onko salasana ja käyttäjänimi oikein
        # ei saa oikeasti tehäd näin jos olisi tuotannossa
        if username == dbinfo.data["admin_username"] and bcrypt.checkpw(password.encode("utf-8"), dbinfo.data["admin_password"]):
            # sulkee log ikkunan
            root.withdraw()
            # avaa admin_window
            admin_window.admin_window(root)
        else:
            # jos salasana tai käyttäjänimi väärin laittaa tekstin
            text.place(x=385, y=235)
            my_string_var.set("Salasana tai käyttäjänimi on väärin")
    except Exception as e:
        # jos jokin menee pieleen tulee teksti
        text.place(x=465, y=235)
        my_string_var.set("Jokin meni vikaan")
    
# luodaan inpu teille tyyppi
username_var= StringVar()
password_var= StringVar()
my_string_var = StringVar()

# otsikko teksti
ctk.CTkLabel(root, text = "Log in", font=('calibre',35,'bold')).place(x=465, y=75)

# name input
username = ctk.CTkLabel(root, text="Name:", font=('calibre',20)).place(x=385, y=150)
username_input = ctk.CTkEntry(root, textvariable=username_var, font=('calibre',20,'normal'), width=200)
username_input.place(x=450, y=150)

# password input
password = ctk.CTkLabel(root, text="Password:", font=('calibre',20)).place(x=350, y=200)
password_input = ctk.CTkEntry(root, textvariable=password_var, font=('calibre',20,'normal'), show="*", width=200)
password_input.place(x=450, y=200)

# luodaan teksti kenttä jossa teksti voi muuttua
my_string_var.set("")
text = ctk.CTkLabel(root, textvariable=my_string_var, font=('calibre',20))
text.place(x=465, y=235)

# luodaan tyylit buttoniin ja luodaan buttoni
button = ctk.CTkButton(master=root, text="Login", command=get_input).place(x=510, y=270)

# jos painaa x:sää sulkee ikkunan
def close():
    root.destroy()
root.protocol("WM_DELETE_WINDOW", close)

if __name__=="__main__":
    root.mainloop()