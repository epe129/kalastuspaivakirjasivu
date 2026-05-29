"""
admin window moduuli on tehty thinker- ja customtkinter:illä,
jossa admin voi poistaa käyttajiä, vieheitä, vapoja ja lajeja.
"""
from tkinter import StringVar, END
from CTkListbox import CTkListbox
import customtkinter as ctk
import pymysql
import dbinfo
import poista_moduuli
import tarkista_moduuli

# yhteys tietokantaan, ottaa yhteyden tiedot python tidostosta
connection = pymysql.connect(host=dbinfo.data["HOST"], port=dbinfo.data["PORT"],
user=dbinfo.data["USER"], password=dbinfo.data["PASSWORD"], database=dbinfo.data["DBNIMI"])
cursor = connection.cursor()

def paikat(paikat_list):
    """
    Asettaa placet parametreista ja laittaa ne for loopilla paikalleen.
    """
    for c, i in paikat_list:
        c.place(x=i["x"], y=i["y"])

def paikat_unohtaa(paikat_list):
    """
    Poistaa asetettuja paikkoja.
    place_forget() poistaa kentä nykyiseltä paikalta
    """
    for c in paikat_list:
        c.place_forget()

def tayttaa_input(hae, box):
    """
    laittaa clikatun valuen inputtiin
    """
    # poistaa kaiken inputista
    hae.delete(0, END)
    # lisää klikatun arvon inputtiin
    hae.insert(0, box.get())

def lisaa_arvot(fetch, l):
    """
    lisää arvot listoihin
    """
    for x in fetch:
        l.append(x[0])

def paivittaa_list_haku(kayttajat_list, box):
    """
    Päivitää listoja jotka näkyy kun hakee inputissa
    """
    try:
        # poistaa kaiken inputista, näin jotta käy yksitellen jokaisen läpi niin ei tuu erroria
        for _ in range(box.size()):
            box.delete(0)
        # lisää arvot uudestaan listaa jotta päivittyy
        for index, item in enumerate(kayttajat_list):
            box.insert(index, item)
    except KeyError:
        pass

def admin_window(root):
    """
    luodaan admin ikkuna ja siihen buttonit, labelit, luettelot ja tekstit.
    lambda: sallii lähettää parametreja kun esim buttoni kutsuu functiota.
    Käytetään frame, jotta kaikki admin_window buttonit,
    label tms ikkunan sisällä pysyvät aina samassa paikassa.
    """
    # luodaan listat
    kayttajat_list = []
    lajit_list = []
    vavat_list = []
    viehet_list = []

    # lisää listoihin arvot tietokannasta jotka näkyy jos käyttäjä käyttää syöttö kenttää
    cursor.execute("SELECT email FROM kalastaja")
    kayttajat = cursor.fetchall()
    lisaa_arvot(kayttajat, kayttajat_list)

    cursor.execute("SELECT laji FROM laji")
    lajit = cursor.fetchall()
    lisaa_arvot(lajit, lajit_list)

    cursor.execute("SELECT vapa FROM vapa")
    vavat = cursor.fetchall()
    lisaa_arvot(vavat, vavat_list)

    cursor.execute("SELECT viehe FROM viehe")
    viehet = cursor.fetchall()
    lisaa_arvot(viehet, viehet_list)

    # luodaan ikkuna
    window = ctk.CTkToplevel(root)
    window.geometry("1000x600")
    window.resizable(width=False, height=False)
    window.title("Admin")
    container = ctk.CTkFrame(window, width=1000, height=600)
    container.place(x=0, y=0)               
    # luodaan inpu teille tyyppit
    hae_string_var = StringVar()
    laji_hae_string_var = StringVar()
    vapa_hae_string_var = StringVar()
    viehe_hae_string_var = StringVar()

    # koko ikkunan otsikko
    ctk.CTkLabel(container, text="Admin", font=('calibre',40)).place(x=450, y=25)

    # otsikko
    ctk.CTkLabel(container, text="Poista käyttäjä:", font=('calibre',20)).place(x=210, y=100)
    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    kayttajat_list_box = CTkListbox(container, width=200)
    # hakukenttä
    hae_kayttaja = ctk.CTkEntry(container, textvariable=hae_string_var,
                                font=('calibre',12,'normal'), width=200)
    hae_kayttaja.place(x=210, y=130)        
    # luettelo boxsi
    kayttajat_input = ctk.CTkComboBox(container, values=[x[0] for x in kayttajat],
                                       font=('calibre',15))
    kayttajat_input.set("Poista käyttäjä")
    kayttajat_input.place(x=210, y=160)
    # button
    button_kayttaja = ctk.CTkButton(master=container ,text="Poista käyttäjä", 
                                    command=lambda: poista_moduuli.kayttaja_poista(
        kayttajat_input,
        hae_kayttaja,
        button_kayttaja,
        text_vapa,
        hae_vapa,
        vapa_input,
        button_vapa,
        vapa_list_box,
        kayttajat_list_box,
        kayttajat_list,
        cursor,
        connection
    ))
    button_kayttaja.place(x=210, y=190)
    # kuuntelee jos kayttajat_list_box arvo klikattu
    kayttajat_list_box.bind("<Button-1>", lambda e: tayttaa_input(hae_kayttaja, kayttajat_list_box))
    # päivittää kayttajat_list_box
    paivittaa_list_haku(kayttajat_list, kayttajat_list_box)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_kayttaja.bind('<KeyRelease>', lambda e: tarkista_moduuli.tarkistaa_input_kayttaja(
        hae_kayttaja,
        kayttajat_list_box,
        button_kayttaja,
        kayttajat_input,
        text_vapa,
        hae_vapa,
        vapa_input,
        button_vapa,
        vapa_list_box,
        kayttajat_list
    ))

    # otsikko
    ctk.CTkLabel(container, text="Poista laji:", font=('calibre',20)).place(x=590, y=100)
    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    laji_list_box = CTkListbox(container, width=200)
    # hakukenttä
    hae_laji = ctk.CTkEntry(container, textvariable=laji_hae_string_var,
                            font=('calibre',12,'normal'), width=200)
    hae_laji.place(x=590, y=130) 
    # luettelo boxsi
    laji_input = ctk.CTkComboBox(container, values=[x[0] for x in lajit], font=('calibre',15))
    laji_input.set("Poista laji")
    laji_input.place(x=590, y=160)
    # button
    button_laji = ctk.CTkButton(master=container ,text="Poista laji",
                                command=lambda: poista_moduuli.laji_poista(
        laji_input,
        hae_laji,
        button_laji,
        text_viehe,
        hae_viehe,
        viehe_input,
        button_viehe,
        viehe_list_box,
        laji_list_box,
        lajit_list,
        cursor,
        connection
    ))
    button_laji.place(x=590, y=190)
    # kuuntelee jos laji_list_box arvo klikattu
    laji_list_box.bind("<Button-1>", lambda e: tayttaa_input(hae_laji, laji_list_box))
    # päivittää laji_list_box
    paivittaa_list_haku(lajit_list, laji_list_box)  
    # kuuntelee jos inputtiin kirjoitetaan
    hae_laji.bind('<KeyRelease>', lambda e: tarkista_moduuli.tarkistaa_input_laji(
        hae_laji,
        laji_list_box,
        button_laji,
        laji_input,
        text_viehe,
        hae_viehe,
        viehe_input,
        button_viehe,
        viehe_list_box,
        lajit_list
    ))

    # otsikko
    text_vapa = ctk.CTkLabel(container, text="Poista vapa:", font=('calibre',20))
    text_vapa.place(x=210, y=250)
    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    vapa_list_box = CTkListbox(container, width=200)
    # hakukenttä
    hae_vapa = ctk.CTkEntry(container, textvariable=vapa_hae_string_var,
                            font=('calibre',12,'normal'), width=200)
    hae_vapa.place(x=210, y=280) 
    # luettelo boxsi
    vapa_input = ctk.CTkComboBox(container, values=[x[0] for x in vavat], font=('calibre',15))
    vapa_input.set("Poista vapa")
    vapa_input.place(x=210, y=310)
    # button
    button_vapa = ctk.CTkButton(master=container ,text="Poista vapa", 
                                command=lambda: poista_moduuli.vapa_poista(
        vapa_input,
        hae_vapa,
        button_vapa,
        vapa_list_box,
        vavat_list,
        cursor,
        connection
    ))
    button_vapa.place(x=210, y=340)
    # kuuntelee jos vapa_list_box arvo klikattu
    vapa_list_box.bind("<Button-1>", lambda e: tayttaa_input(hae_vapa, vapa_list_box))
    # päivittää vapa_list_box
    paivittaa_list_haku(vavat_list, vapa_list_box)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_vapa.bind('<KeyRelease>', lambda e: tarkista_moduuli.tarkistaa_input_vapa(
        hae_vapa,
        vapa_list_box,
        button_vapa,
        vapa_input,
        vavat_list
    ))

    # otsikko
    text_viehe = ctk.CTkLabel(container, text="Poista viehe:", font=('calibre',20))
    text_viehe.place(x=590, y=250)
    # luodaan luettelo jossa näkyy arvot jos käyttää haku kenttää
    viehe_list_box = CTkListbox(container, width=200)
    # hakukenttä
    hae_viehe = ctk.CTkEntry(container, textvariable=viehe_hae_string_var, 
                            font=('calibre',12,'normal'), width=200)
    hae_viehe.place(x=590, y=280) 
    # luettelo boxsi
    viehe_input = ctk.CTkComboBox(container, values=[x[0] for x in viehet], font=('calibre',15))
    viehe_input.set("Poista viehe")
    viehe_input.place(x=590, y=310)
    # button
    button_viehe = ctk.CTkButton(master=container ,text="Poista viehe", 
                                 command=lambda: poista_moduuli.viehe_poista(
        viehe_input,
        hae_viehe,
        button_viehe,
        viehe_list_box,
        viehet_list, 
        cursor,
        connection
    ))
    button_viehe.place(x=590, y=340)
    # kuuntelee jos viehe_list_box arvo klikattu
    viehe_list_box.bind("<Button-1>", lambda e: tayttaa_input(hae_viehe, viehe_list_box))
    # päivittää viehe_list_box
    paivittaa_list_haku(viehet_list, viehe_list_box)
    # kuuntelee jos inputtiin kirjoitetaan
    hae_viehe.bind('<KeyRelease>', lambda e: tarkista_moduuli.tarkistaa_input_viehe(
        hae_viehe,
        viehe_list_box,
        button_viehe,
        viehe_input,
        viehet_list
    ))

    def close():
        """
        Jos painaa x:sää sulkee ikkunan.
        """
        root.destroy()
    window.protocol("WM_DELETE_WINDOW", close)
