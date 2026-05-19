import bcrypt
import customtkinter as ctk
import pymysql, dbinfo
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from CTkListbox import CTkListbox

# yhteys tietokantaan, ottaa yhteyden tiedot python tidostosta
connection = pymysql.connect(host=dbinfo.data["HOST"], port=dbinfo.data["PORT"], user=dbinfo.data["USER"], password=dbinfo.data["PASSWORD"], database=dbinfo.data["DBNIMI"])
cursor = connection.cursor()

# laitta ohjelmalle systeemin 
ctk.set_appearance_mode("System") 

# luodaan ikkuna
root = ctk.CTk()
root.geometry("1000x600")
root.resizable(width=False, height=False)
root.title("Admin")

def admin_window():
    # luodaan listat
    kayttajat_list = []
    lajit_list = []
    vavat_list = []
    viehet_list = []

    # luodaan ikkuna
    admin_window = ctk.CTkToplevel(root)
    admin_window.geometry("1000x600")  
    admin_window.resizable(width=False, height=False)
    admin_window.title("Admin")
    # luodaan frame, kaikki admin_window buttonit, label tms ob täb sisällä jotta pysyvät aina samassa paikassa
    container = ctk.CTkFrame(admin_window, width=1000, height=600)
    container.place(x=0, y=0)
    
    # tapahtuu käyttäjän poisto
    def kayttaja_poista():
        # tarkistaa kummasta ottaa arvon input vai valikosta 
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
        # päivittää listat ja luettelot
        cursor.execute(f"SELECT email FROM kalastaja")
        kayttajat = cursor.fetchall()
        kayttajat_input.configure(values=[x[0] for x in kayttajat])
        kayttajat_input.set("Poista käyttäjä")
        kayttajat_list.clear()
        for x in kayttajat:
            kayttajat_list.append(x[0])

    # tapahtuu lajin poisto
    def laji_poista():
        # tarkistaa kummasta ottaa arvon input vai valikosta 
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
        # poistetaan laji ja siihen kuuluvat tiedot
        cursor.execute(f"SELECT id FROM laji WHERE laji='{saa_laji_input[0]}'")
        laji_id = cursor.fetchall()
        cursor.execute(f"DELETE FROM kala WHERE laji_id ='{laji_id}'")        
        cursor.execute(f"DELETE FROM laji WHERE laji='{saa_laji_input[0]}'")        
        # tallettaa tapahtuneen tietokantaan
        connection.commit()
        # päivittää listat ja luettelot
        cursor.execute(f"SELECT laji FROM laji")
        lajit = cursor.fetchall()
        laji_input.configure(values=[x[0] for x in lajit])
        laji_input.set("Poista käyttäjä")
        lajit_list.clear()
        for x in lajit:
            lajit_list.append(x[0])

    # tapahtuu vavan poisto
    def vapa_poista():
        # tarkistaa kummasta ottaa arvon input vai valikosta 
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
        # päivittää listat ja luettelot
        cursor.execute(f"SELECT vapa FROM vapa")
        vavat = cursor.fetchall()
        vapa_input.configure(values=[x[0] for x in vavat])
        vapa_input.set("Poista vapa")
        vavat_list.clear()
        for x in vavat:
            vavat_list.append(x[0])

    # tapahtuu viehen poisto
    def viehe_poista():
        # tarkistaa kummasta ottaa arvon input vai valikosta 
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
        # päivittää listat ja luettelot
        cursor.execute(f"SELECT viehe FROM viehe")
        viehet = cursor.fetchall()
        viehe_input.configure(values=[x[0] for x in viehet])
        viehe_input.set("Poista viehe")
        viehet_list.clear()
        for x in viehet:
            viehet_list.append(x[0])

    # ------------------------------------------------------------------ #

    # lisää listoihin arvot tietokannasta jotka näkyy jos käyttäjä käyttää syöttö kenttää
    cursor.execute(f"SELECT email FROM kalastaja")
    kayttajat = cursor.fetchall()
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

    # ------------------------------------------------------------------ #

    # päivitää listaa joka näkyy kun hakee inputissa
    def paivittaa_list_kayttaja(kayttajat_list):
        # poistaa kaiken inputista, näin jotta käy yksitellen jokaisen läpi niin ei tuu erroria
        for _ in range(kayttajat_list_box.size()):
            kayttajat_list_box.delete(0)
        # lisää arvot uudestaan listaa jotta päivittyy
        for item in kayttajat_list:
            kayttajat_list_box.insert(END, item)
    # päivitää listaa joka näkyy kun hakee inputissa
    def paivittaa_list_laji(lajit_list):
        # poistaa kaiken inputista        
        for _ in range(laji_list_box.size()):
            laji_list_box.delete(0)        
        # lisää arvot uudestaan listaa jotta päivittyy
        for item in lajit_list:
            laji_list_box.insert(END, item)
    # päivitää listaa joka näkyy kun hakee inputissa
    def paivittaa_list_viehe(viehet_list):
        # poistaa kaiken inputista
        for _ in range(viehe_list_box.size()):
            viehe_list_box.delete(0)
        # lisää arvot uudestaan listaa jotta päivittyy
        for item in viehet_list:
            viehe_list_box.insert(END, item)
    # päivitää listaa joka näkyy kun hakee inputissa
    def paivittaa_list_vapa(vapa_list):
        # poistaa kaiken inputista
        for _ in range(vapa_list_box.size()):
            vapa_list_box.delete(0)
        # lisää arvot uudestaan listaa jotta päivittyy
        for item in vapa_list:
            vapa_list_box.insert(END, item)

    # ------------------------------------------------------------------ #

    # laittaa clikatun valuen inputtiin
    def tayttaa_input_kayttaja(e):
        # poistaa kaiken inputista
        hae_kayttaja.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_kayttaja.insert(0, kayttajat_list_box.get())
    
    def tayttaa_input_laji(e):
        # poistaa kaiken inputista
        hae_laji.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_laji.insert(0, laji_list_box.get())

    def tayttaa_input_viehe(e):
        # poistaa kaiken inputista
        hae_viehe.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_viehe.insert(0, viehe_list_box.get())

    def tayttaa_input_vapa(e):
        # poistaa kaiken inputista
        hae_vapa.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_vapa.insert(0, vapa_list_box.get())

    # ------------------------------------------------------------------ #

    # entery boxin eli input ja päivittää listaa haun mukaan
    def tarkistaa_input_kayttaja(event):
        # muokka kenttien ja nappin paikkoja sekä saa inputin
        hae_kayttaja_input = hae_kayttaja.get()
        kayttajat_list_box.place(x=210, y=165)
        kayttajat_input.place(x=-210, y=-165)
        button_kayttaja.place(x=423, y=130)

        # laitetaan vapa teksti pois tieltä
        text_vapa.place(x=-210, y=-190)
        hae_vapa.place(x=-210, y=-190) 
        vapa_input.place(x=-210, y=-190)
        button_vapa.place(x=-210, y=-190)
        vapa_list_box.place(x=-210, y=-190)
        # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
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
            # kun kirjoittaa inputtiin hakee tietoa ja rajaa sillä jos sana/kirjaimet on jossain arvossa
            data_kayttaja = []
            for item in kayttajat_list:
                if hae_kayttaja_input.lower() in str(item).lower():
                    data_kayttaja.append(item)
        # päivittää listaa joka näkyy kun hakee haun perusteella
        paivittaa_list_kayttaja(data_kayttaja)
        
    def tarkistaa_input_laji(event):
        # muokka kenttien ja nappin paikkoja sekä saa inputin
        laji_kayttaja_input = hae_laji.get()
        laji_list_box.place(x=590, y=165)
        laji_input.place(x=-210, y=-165)
        button_laji.place(x=803, y=130)
        # laitetaan viehe teksti pois tieltä
        text_viehe.place(x=-210, y=-190)
        hae_viehe.place(x=-210, y=-190) 
        viehe_input.place(x=-210, y=-190)
        button_viehe.place(x=-210, y=-190)
        viehe_list_box.place(x=-210, y=-190)
        # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
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
            # kun kirjoittaa inputtiin hakee tietoa ja rajaa sillä jos sana/kirjaimet on jossain arvossa
            data_laji = []
            for item in lajit_list:
                if laji_kayttaja_input.lower() in str(item).lower():
                    data_laji.append(item)     
        # päivittää listaa joka näkyy kun hakee haun perusteella
        paivittaa_list_laji(data_laji)
    
    def tarkistaa_input_viehe(event):
        # muokka kenttien ja nappin paikkoja sekä saa inputin
        viehe_kayttaja_input = hae_viehe.get()
        viehe_list_box.place(x=590, y=310)
        viehe_input.place(x=-210, y=-165)
        button_viehe.place(x=803, y=280)
        # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
        if viehe_kayttaja_input == '':
            data_viehe = viehet_list
            viehe_input.place(x=590, y=310)
            button_viehe.place(x=590, y=340)
            viehe_list_box.place(x=-210, y=-190)
            viehe_input.set("Poista viehe")
            hae_viehe.delete(0, END)
        else:
            # kun kirjoittaa inputtiin hakee tietoa ja rajaa sillä jos sana/kirjaimet on jossain arvossa
            data_viehe = []
            for item in viehet_list:
                if viehe_kayttaja_input.lower() in str(item).lower():
                    data_viehe.append(item)
        # päivittää listaa joka näkyy kun hakee haun perusteella
        paivittaa_list_viehe(data_viehe)

    def tarkistaa_input_vapa(event):
        # muokka kenttien ja nappin paikkoja sekä saa inputin
        vapa_input_hae = hae_vapa.get()
        vapa_list_box.place(x=210, y=310)
        vapa_input.place(x=-210, y=-165)
        button_vapa.place(x=423, y=280)
        # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
        if vapa_input_hae == '':
            data_vapa = vavat_list
            vapa_input.place(x=210, y=310)
            button_vapa.place(x=210, y=340)
            vapa_list_box.place(x=-210, y=-190)
            vapa_input.set("Poista viehe")
            hae_vapa.delete(0, END)
        else:
            # kun kirjoittaa inputtiin hakee tietoa ja rajaa sillä jos sana/kirjaimet on jossain arvossa
            data_vapa = []
            for item in vavat_list:
                if vapa_input_hae.lower() in str(item).lower():
                    data_vapa.append(item)
        # päivittää listaa joka näkyy kun hakee haun perusteella
        paivittaa_list_vapa(data_vapa)

    # ------------------------------------------------------------------ #
    # luodaan inpu teille tyyppi
    hae_string_var = StringVar()
    laji_hae_string_var = StringVar()
    vapa_hae_string_var = StringVar()
    viehe_hae_string_var = StringVar()

    # ------------------------------------------------------------------ #

    # koko ikkunan otsikko
    text_admin = ctk.CTkLabel(container, text="Admin", font=('calibre',40)).place(x=450, y=25)

    # ------------------------------------------------------------------ #

    # alkaa käyttäjä 
    # otsikko
    text_kayttaja = ctk.CTkLabel(container, text="Poista käyttäjä:", font=('calibre',20)).place(x=210, y=100)

    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    kayttajat_list_box = CTkListbox(container, width=200)

    # hakukenttä
    hae_kayttaja = ctk.CTkEntry(container, textvariable=hae_string_var, font=('calibre',12,'normal'), width=200)
    hae_kayttaja.place(x=210, y=130)        

    # luettelo boxsi
    kayttajat_input = ctk.CTkComboBox(container, values=[x[0] for x in kayttajat], font=('calibre',15))
    kayttajat_input.set("Poista käyttäjä")
    kayttajat_input.place(x=210, y=160)

    # button
    button_kayttaja = ctk.CTkButton(master=container ,text="Poista käyttäjä", command=kayttaja_poista)
    button_kayttaja.place(x=210, y=190)
    

    # kuuntelee jos kayttajat_list_box arvo klikattu
    kayttajat_list_box.bind("<Button-1>", tayttaa_input_kayttaja)
    # päivittää kayttajat_list_box
    paivittaa_list_kayttaja(kayttajat_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_kayttaja.bind('<KeyRelease>', tarkistaa_input_kayttaja)
    
    # ------------------------------------------------------------------ #

    # alkaa laji
    # otsikko
    text_laji = ctk.CTkLabel(container, text="Poista laji:", font=('calibre',20)).place(x=590, y=100)
    
    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    laji_list_box = CTkListbox(container, width=200)

    # hakukenttä
    hae_laji = ctk.CTkEntry(container, textvariable=laji_hae_string_var, font=('calibre',12,'normal'), width=200)
    hae_laji.place(x=590, y=130) 

    # luettelo boxsi
    laji_input = ctk.CTkComboBox(container, values=[x[0] for x in lajit], font=('calibre',15))
    laji_input.set("Poista laji")
    laji_input.place(x=590, y=160)

    # button
    button_laji = ctk.CTkButton(master=container ,text="Poista laji", command=laji_poista)
    button_laji.place(x=590, y=190)

    # kuuntelee jos laji_list_box arvo klikattu
    laji_list_box.bind("<Button-1>", tayttaa_input_laji)
    # päivittää laji_list_box
    paivittaa_list_laji(lajit_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_laji.bind('<KeyRelease>', tarkistaa_input_laji)

    # ------------------------------------------------------------------ #

    # alkaa vapa 
    # otsikko
    text_vapa = ctk.CTkLabel(container, text="Poista vapa:", font=('calibre',20))
    text_vapa.place(x=210, y=250)

    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    vapa_list_box = CTkListbox(container, width=200)

    # hakukenttä
    hae_vapa = ctk.CTkEntry(container, textvariable=vapa_hae_string_var, font=('calibre',12,'normal'), width=200)
    hae_vapa.place(x=210, y=280) 

    # luettelo boxsi
    vapa_input = ctk.CTkComboBox(container, values=[x[0] for x in vavat], font=('calibre',15))
    vapa_input.set("Poista vapa")
    vapa_input.place(x=210, y=310)
    
    # button
    button_vapa = ctk.CTkButton(master=container ,text="Poista vapa", command=vapa_poista)
    button_vapa.place(x=210, y=340)

    # kuuntelee jos vapa_list_box arvo klikattu
    vapa_list_box.bind("<Button-1>", tayttaa_input_vapa)
    # päivittää vapa_list_box
    paivittaa_list_vapa(vavat_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_vapa.bind('<KeyRelease>', tarkistaa_input_vapa)

    # ------------------------------------------------------------------ #

    # alkaa viehe
    # otsikko
    text_viehe = ctk.CTkLabel(container, text="Poista viehe:", font=('calibre',20))
    text_viehe.place(x=590, y=250)

    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    viehe_list_box = CTkListbox(container, width=200)
    
    # hakukenttä
    hae_viehe = ctk.CTkEntry(container, textvariable=viehe_hae_string_var, font=('calibre',12,'normal'), width=200)
    hae_viehe.place(x=590, y=280) 

    # luettelo boxsi
    viehe_input = ctk.CTkComboBox(container, values=[x[0] for x in viehet], font=('calibre',15))
    viehe_input.set("Poista viehe")
    viehe_input.place(x=590, y=310)
    
    # button
    button_viehe = ctk.CTkButton(master=container ,text="Poista viehe", command=viehe_poista)
    button_viehe.place(x=590, y=340)
    
    # kuuntelee jos viehe_list_box arvo klikattu
    viehe_list_box.bind("<Button-1>", tayttaa_input_viehe)
    # päivittää viehe_list_box
    paivittaa_list_viehe(viehet_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_viehe.bind('<KeyRelease>', tarkistaa_input_viehe)

    # ------------------------------------------------------------------ #

    # jos painaa x:sää sulkee ikkunan, pitää olla molemmat koska root.withdraw() ei sulje ikkunaa kokonaan vain piilottaa
    def close():
        root.destroy()
    admin_window.protocol("WM_DELETE_WINDOW", close)

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
            admin_window()
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
l = ctk.CTkLabel(root, text = "Log in", font=('calibre',35,'bold')).place(x=465, y=75)

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