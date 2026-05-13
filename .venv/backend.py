import bcrypt
import customtkinter as ctk
import pymysql, dbinfo
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *

# otetaan db tiedot python tiedostosta
USER = dbinfo.data["USER"]
PASSWORD = dbinfo.data["PASSWORD"]
DBNIMI = dbinfo.data["DBNIMI"]
PORT = dbinfo.data["PORT"]
HOST = dbinfo.data["HOST"]

# yhteys tietokantaan
connection = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DBNIMI)
cursor = connection.cursor()
# laitta ohjelmalle systeemin teeman eli tumma tai vaalea
ctk.set_appearance_mode("System") 

# luodaan ikkuna
root = ctk.CTk()
root.resizable(width=False, height=False)
root.geometry("600x600")
root.title("Admin")

def admin_window():
    kayttajat_list = []
    lajit_list = []
    vavat_list = []
    viehet_list = []
    
    ctk.set_appearance_mode("System") 
    admin_window = ctk.CTk()
    admin_window.geometry("1000x600")  
    admin_window.resizable(width=False, height=False)
    admin_window.title("Admin")
    # window_width = admin_window.winfo_width()
    # käytetään käyttäjän poistoon
    def kayttaja_poista():
        # tarkistaa kummasta ottaa input vai valikosta arvon
        kayttaja_poista = kayttajat_input.get().split()
        if kayttaja_poista == "" or "Poista" in kayttaja_poista:
            kayttaja_poista = hae_kayttaja.get().split()
            kayttajat_input.place(x=10, y=160)  
            button_kayttaja.place(x=10, y=190)
            kayttajat_list_box.place(x=-10, y=-190)
            kayttajat_input.set("Poista käyttäjä")
            hae_kayttaja.delete(0, END)
            # laitetaan vapa tekstit takasin paikalleen
            text_vapa.place(x=210, y=250)
            hae_vapa.place(x=210, y=280) 
            vapa_input.place(x=210, y=310)
            button_vapa.place(x=210, y=340)
            vapa_list_box.place(x=-210, y=-190)

        # poistetaan käyttäjä ja siihen kuuluvat tiedot
        cursor.execute(f"SELECT id FROM kalastaja WHERE email='{kayttaja_poista[0]}'")
        kayttajat_id = cursor.fetchall()
        
        cursor.execute(f"SELECT id FROM tarppi WHERE kalastaja_id='{kayttajat_id[0][0]}'")
        tarppi_idt = cursor.fetchall()
        for c in tarppi_idt:
            cursor.execute(f"DELETE FROM kala WHERE tarppi_id='{c[0]}'")
        cursor.execute(f"DELETE FROM tarppi WHERE kalastaja_id='{kayttajat_id[0][0]}'")
        cursor.execute(f"DELETE FROM kalastaja WHERE email='{kayttaja_poista[0]}'")
        
        # tallettaa tapahtuneen tietokantaan
        connection.commit()
        cursor.execute(f"SELECT email FROM kalastaja")
        kayttajat = cursor.fetchall()
        kayttajat_input.configure(values=[x[0] for x in kayttajat])
        kayttajat_input.set("Poista käyttäjä")
        kayttajat_list.clear()
        for x in kayttajat:
            kayttajat_list.append(x[0])

    # poistetaan laji, vapa tai viehe 
    def laji_poista():
        saa_laji_input = laji_input.get().split()
        if saa_laji_input == "" or "Poista" in saa_laji_input:
            saa_laji_input = hae_laji.get().split()
            laji_input.place(x=590, y=160)
            button_laji.place(x=590, y=190)
            laji_list_box.place(x=-10, y=-190)
            laji_input.set("Poista laji")
            hae_laji.delete(0, END)
            # laitetaan viehet tekstit takasin paikalleen
            text_viehe.place(x=590, y=250)
            hae_viehe.place(x=590, y=280) 
            viehe_input.place(x=590, y=310)
            button_viehe.place(x=590, y=340)
            viehe_list_box.place(x=-210, y=-190)
        cursor.execute(f"DELETE FROM laji WHERE laji='{saa_laji_input[0]}'")        
        # tallettaa tapahtuneen tietokantaan
        connection.commit()
        cursor.execute(f"SELECT laji FROM laji")
        lajit = cursor.fetchall()
        laji_input.configure(values=[x[0] for x in lajit])
        laji_input.set("Poista käyttäjä")
        lajit_list.clear()
        for x in lajit:
            lajit_list.append(x[0])

    def vapa_poista():
        saa_vapa_input = vapa_input.get().split()
        if saa_vapa_input == "" or "Poista" in saa_vapa_input:
                saa_vapa_input = hae_vapa.get().split()
                vapa_input.place(x=210, y=310)
                button_vapa.place(x=210, y=340)
                vapa_list_box.place(x=-10, y=-190)
                vapa_input.set("Poista viehe")
                hae_vapa.delete(0, END)
        cursor.execute(f"DELETE FROM vapa WHERE vapa='{saa_vapa_input[0]}'")        
        # tallettaa tapahtuneen tietokantaan
        connection.commit()
        cursor.execute(f"SELECT vapa FROM vapa")
        vavat = cursor.fetchall()
        vapa_input.configure(values=[x[0] for x in vavat])
        vapa_input.set("Poista vapa")
        vavat_list.clear()
        for x in vavat_list:
            vavat_list.append(x[0])


    def viehe_poista():
        saa_viehe_input = viehe_input.get().split()
        if saa_viehe_input == "" or "Poista" in saa_viehe_input:
            saa_viehe_input = hae_viehe.get().split()
            viehe_input.place(x=590, y=310)
            button_viehe.place(x=590, y=340)
            viehe_list_box.place(x=-10, y=-190)
            viehe_input.set("Poista viehe")
            hae_viehe.delete(0, END)
        cursor.execute(f"DELETE FROM viehe WHERE viehe='{saa_viehe_input[0]}'")        
        # tallettaa tapahtuneen tietokantaan
        connection.commit()
        cursor.execute(f"SELECT viehe FROM viehe")
        viehet = cursor.fetchall()
        viehe_input.configure(values=[x[0] for x in viehet])
        viehe_input.set("Poista viehe")
        viehet_list.clear()
        for x in viehet:
            viehet_list.append(x[0])


    # oteteaan data tietokannasat
    cursor.execute(f"SELECT email FROM kalastaja")
    kayttajat = cursor.fetchall()
    # lisää käyttäjät listaan joka näkyy jos käyttää syöttö kenttää
    for x in kayttajat:
        kayttajat_list.append(x[0])

    cursor.execute(f"SELECT laji FROM laji")
    lajit = cursor.fetchall()
    for l in lajit:
        lajit_list.append(l[0])

    cursor.execute(f"SELECT vapa FROM vapa")
    vavat = cursor.fetchall()
    for va in vavat:
        vavat_list.append(va[0])

    cursor.execute(f"SELECT viehe FROM viehe")
    viehet = cursor.fetchall()
    for vi in viehet:
        viehet_list.append(vi[0])

    # otsikko
    text_admin = ctk.CTkLabel(admin_window, text="Admin", font=('calibre',40))
    text_admin.place(x=450, y=25)
    # luodaan lista 
    kayttajat_list_box = Listbox(admin_window, width=50)

    # käyttäjän poisto
    # otsikko
    text_kayttaja = ctk.CTkLabel(admin_window, text="Poista käyttäjä:", font=('calibre',20))
    text_kayttaja.place(x=210, y=100)

    hae_string_var = StringVar()
    hae_kayttaja = tk.Entry(admin_window, textvariable=hae_string_var, font=('calibre',12,'normal'), width=25)
    hae_kayttaja.place(x=210, y=130)        

    # päivitää listaa
    def paivittaa_list_kayttaja(kayttajat_list):
        kayttajat_list_box.delete(0, END)
        for item in kayttajat_list:
            kayttajat_list_box.insert(END, item)

    def paivittaa_list_laji(lajit_list):
        laji_list_box.delete(0, END)
        for item in lajit_list:
            laji_list_box.insert(END, item)

    def paivittaa_list_viehe(viehet_list):
        viehe_list_box.delete(0, END)
        for item in viehet_list:
            viehe_list_box.insert(END, item)

    def paivittaa_list_vapa(vapa_list):
        vapa_list_box.delete(0, END)
        for item in vapa_list:
            vapa_list_box.insert(END, item)

    # laittaa clikatun valuen inputtiin
    def tayttaa_input_kayttaja(e):
        # poistaa kaiken inputista
        hae_kayttaja.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_kayttaja.insert(0, kayttajat_list_box.get(ANCHOR))
    
    def tayttaa_input_laji(e):
        # poistaa kaiken inputista
        hae_laji.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_laji.insert(0, laji_list_box.get(ANCHOR))

    def tayttaa_input_viehe(e):
        # poistaa kaiken inputista
        hae_viehe.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_viehe.insert(0, viehe_list_box.get(ANCHOR))

    def tayttaa_input_vapa(e):
        # poistaa kaiken inputista
        hae_vapa.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_vapa.insert(0, vapa_list_box.get(ANCHOR))

    # entery boxin ja päivittää listaa haun mukaan
    def tarkistaa_input_kayttaja(event):
        # muokka kenttien ja nappin paikkoja
        hae_kayttaja_input = hae_kayttaja.get()
        kayttajat_list_box.place(x=210, y=165)
        kayttajat_input.place(x=-210, y=-165)
        button_kayttaja.place(x=443, y=128)
        # laitetaan vapa teksti pois tieltä
        text_vapa.place(x=-210, y=-190)
        hae_vapa.place(x=-210, y=-190) 
        vapa_input.place(x=-210, y=-190)
        button_vapa.place(x=-210, y=-190)
        vapa_list_box.place(x=-210, y=-190)


        if hae_kayttaja_input == '':
            data_kayttaja = kayttajat_list
            kayttajat_input.place(x=210, y=160)  
            button_kayttaja.place(x=210, y=190)
            kayttajat_list_box.place(x=-210, y=-190)
            kayttajat_input.set("Poista käyttäjä")
            hae_kayttaja.delete(0, END)
            # laitetaan vapa tekstit takasin paikalleen
            text_vapa.place(x=210, y=250)
            hae_vapa.place(x=210, y=280) 
            vapa_input.place(x=210, y=310)
            button_vapa.place(x=210, y=340)
            vapa_list_box.place(x=-210, y=-190)
        else:
            data_kayttaja = []
            for item in kayttajat_list:
                if hae_kayttaja_input.lower() in item.lower():
                    data_kayttaja.append(item)

        paivittaa_list_kayttaja(data_kayttaja)
        
       
    def tarkistaa_input_laji(event):
        laji_kayttaja_input = hae_laji.get()
        laji_list_box.place(x=590, y=165)
        laji_input.place(x=-210, y=-165)
        button_laji.place(x=823, y=128)
        # laitetaan viehe teksti pois tieltä
        text_viehe.place(x=-210, y=-190)
        hae_viehe.place(x=-210, y=-190) 
        viehe_input.place(x=-210, y=-190)
        button_viehe.place(x=-210, y=-190)
        viehe_list_box.place(x=-210, y=-190)
                    
        if laji_kayttaja_input == '':
            data_laji = lajit_list
            laji_input.place(x=590, y=160)
            button_laji.place(x=590, y=190)
            laji_list_box.place(x=-210, y=-190)
            laji_input.set("Poista laji")
            hae_laji.delete(0, END)
            # laitetaan viehet tekstit takasin paikalleen
            text_viehe.place(x=590, y=250)
            hae_viehe.place(x=590, y=280) 
            viehe_input.place(x=590, y=310)
            button_viehe.place(x=590, y=340)
            viehe_list_box.place(x=-210, y=-190)

        else:
            data_laji = []
            for item in lajit_list:
                if laji_kayttaja_input.lower() in item.lower():
                    data_laji.append(item)
        
        paivittaa_list_laji(data_laji)
    
    def tarkistaa_input_viehe(event):
        viehe_kayttaja_input = hae_viehe.get()
        viehe_list_box.place(x=590, y=310)
        viehe_input.place(x=-210, y=-165)
        button_viehe.place(x=823, y=280)
            
        if viehe_kayttaja_input == '':
            data_viehe = viehet_list
            viehe_input.place(x=590, y=310)
            button_viehe.place(x=590, y=340)
            viehe_list_box.place(x=-210, y=-190)
            viehe_input.set("Poista viehe")
            hae_viehe.delete(0, END)
        else:
            data_viehe = []
            for item in viehet_list:
                if viehe_kayttaja_input.lower() in item.lower():
                    data_viehe.append(item)
        
        paivittaa_list_viehe(data_viehe)


    def tarkistaa_input_vapa(event):
        vapa_input_hae = hae_vapa.get()
        vapa_list_box.place(x=210, y=310)
        vapa_input.place(x=-210, y=-165)
        button_vapa.place(x=443, y=280)

        if vapa_input_hae == '':
            data_vapa = vavat_list
            vapa_input.place(x=210, y=310)
            button_vapa.place(x=210, y=340)
            vapa_list_box.place(x=-210, y=-190)
            vapa_input.set("Poista viehe")
            hae_vapa.delete(0, END)
        else:
            data_vapa = []
            for item in vavat_list:
                if vapa_input_hae.lower() in item.lower():
                    data_vapa.append(item)
        
        paivittaa_list_vapa(data_vapa)
        
    
    # kuuntelee jos hiiren mouse 1 on painettu
    kayttajat_list_box.bind("<Button-1>", tayttaa_input_kayttaja)
    paivittaa_list_kayttaja(kayttajat_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_kayttaja.bind('<Key>', tarkistaa_input_kayttaja)
    
    # luettelo boxsi
    kayttajat_input = ctk.CTkComboBox(admin_window, values=[x[0] for x in kayttajat], font=('calibre',15))
    kayttajat_input.set("Poista käyttäjä")
    kayttajat_input.place(x=210, y=160)
    # button
    button_kayttaja = ctk.CTkButton(master=admin_window ,text="Poista käyttäjä", command=kayttaja_poista)
    button_kayttaja.place(x=210, y=190)

    # alkaa laji
    # laji poisto
    # otsikko
    text_laji = ctk.CTkLabel(admin_window, text="Poista laji:", font=('calibre',20))
    text_laji.place(x=590, y=100)
    
    # luodaan lista 
    laji_list_box = Listbox(admin_window, width=50)

    laji_hae_string_var = StringVar()
    hae_laji = tk.Entry(admin_window, textvariable=laji_hae_string_var, font=('calibre',12,'normal'), width=25)
    hae_laji.place(x=590, y=130) 

    # luettelo boxsi
    laji_input = ctk.CTkComboBox(admin_window, values=[x[0] for x in lajit], font=('calibre',15))
    laji_input.set("Poista laji")
    laji_input.place(x=590, y=160)
    # button
    button_laji = ctk.CTkButton(master=admin_window ,text="Lähetä", command=laji_poista)
    button_laji.place(x=590, y=190)

    laji_list_box.bind("<Button-1>", tayttaa_input_laji)
    paivittaa_list_laji(lajit_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_laji.bind('<Key>', tarkistaa_input_laji)
    # päätyy laji

    # vapa poisto
    # otsikko
    text_vapa = ctk.CTkLabel(admin_window, text="Poista vapa:", font=('calibre',20))
    text_vapa.place(x=210, y=250)

    vapa_list_box = Listbox(admin_window, width=50)
    # input
    vapa_hae_string_var = StringVar()
    hae_vapa = tk.Entry(admin_window, textvariable=vapa_hae_string_var, font=('calibre',12,'normal'), width=25)
    hae_vapa.place(x=210, y=280) 

    # luettelo boxsi
    vapa_input = ctk.CTkComboBox(admin_window, values=[x[0] for x in vavat], font=('calibre',15))
    vapa_input.set("Poista vapa")
    vapa_input.place(x=210, y=310)
    # button
    button_vapa = ctk.CTkButton(master=admin_window ,text="Lähetä", command=vapa_poista)
    button_vapa.place(x=210, y=340)

    vapa_list_box.bind("<Button-1>", tayttaa_input_vapa)
    paivittaa_list_vapa(vavat_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_vapa.bind('<Key>', tarkistaa_input_vapa)
    # päätyy vapa

    # viehe poisto
    # otsikko
    text_viehe = ctk.CTkLabel(admin_window, text="Poista viehe:", font=('calibre',20))
    text_viehe.place(x=590, y=250)

    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    viehe_list_box = Listbox(admin_window, width=50)
    
    # input
    viehe_hae_string_var = StringVar()
    hae_viehe = tk.Entry(admin_window, textvariable=viehe_hae_string_var, font=('calibre',12,'normal'), width=25)
    hae_viehe.place(x=590, y=280) 

    # luettelo boxsi
    viehe_input = ctk.CTkComboBox(admin_window, values=[x[0] for x in viehet], font=('calibre',15))
    viehe_input.set("Poista viehe")
    viehe_input.place(x=590, y=310)
    
    # button
    button_viehe = ctk.CTkButton(master=admin_window ,text="Lähetä", command=viehe_poista)
    button_viehe.place(x=590, y=340)
        
    viehe_list_box.bind("<Button-1>", tayttaa_input_viehe)
    paivittaa_list_viehe(viehet_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_viehe.bind('<Key>', tarkistaa_input_viehe)
    # päätyy viehe

    # jos painaa x:sää sulkee ikkunan, pitää olla molemmat koska root.withdraw() ei sulje ikkunaa kokonaan vain piilottaa
    def close():
        admin_window.destroy()
        root.destroy()
    admin_window.protocol("WM_DELETE_WINDOW", close)
    admin_window.mainloop()

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
            # avaa "hallinta ikkunan"
            admin_window()
        else:
            # jos salasana tai käyttäjänimi väärin laittaa tekstin
            text.place(x=window_width + 20, y=170)
            my_string_var.set("Salasana tai käyttäjänimi on väärin")
    except Exception as e:
        # jos jokin menee pieleen tulee teksti
        text.place(x=window_width + 70, y=170)
        my_string_var.set("Jokin meni vikaan")
    
# saa näytön leveyden
window_width = root.winfo_width()

# luodaan inpu teille tyyppi
username_var=tk.StringVar()
password_var=tk.StringVar()
my_string_var = StringVar()

# otsikko teksti
l = ctk.CTkLabel(root, text = "Log in", font=('calibre',25,'bold'))
l.place(x=window_width + 100, y=75)

# name input
username = ctk.CTkLabel(root, text="Name:", font=('calibre',15))
username_input = tk.Entry(root, textvariable=username_var, font=('calibre',12,'normal'), width=25)
username.place(x=window_width - 23, y=115)
username_input.place(x=window_width + 25, y=115)

# password input
password = ctk.CTkLabel(root, text="Password:", font=('calibre',15))
password_input = tk.Entry(root, textvariable=password_var, font=('calibre',12,'normal'), show="*", width=25)
password.place(x=window_width - 50, y=145)
password_input.place(x=window_width + 25, y=145)

# luodaan teksti kenttä jossa teksti voi muuttua
my_string_var.set("")
text = ctk.CTkLabel(root, textvariable=my_string_var, font=('calibre',15))
text.place(x=window_width + 70, y=170)

# luodaan tyylit buttoniin ja luodaan buttoni
button = ctk.CTkButton(master=root, text="Login", command=get_input)
button.place(x=window_width + 115, y=200)

# jos painaa x:sää sulkee ikkunan
def close():
    root.destroy()
root.protocol("WM_DELETE_WINDOW", close)

if __name__=="__main__":
    root.mainloop()