"""
admin window moduuli joka on tehty thinker- ja customtkinter:illä,
on ikkuna jossa admin voi poistaa käyttajiä, vieheitä, vapoja ja lajeja.
"""
import pymysql, dbinfo
import customtkinter as ctk
from tkinter import StringVar, END
from CTkListbox import CTkListbox

# yhteys tietokantaan, ottaa yhteyden tiedot python tidostosta
connection = pymysql.connect(host=dbinfo.data["HOST"], port=dbinfo.data["PORT"], user=dbinfo.data["USER"], password=dbinfo.data["PASSWORD"], database=dbinfo.data["DBNIMI"])
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

def paivittaa(fetch, i, l):
    """
    Päivittää listat ja luettelot, saa arvot parametreista.
    """
    i.configure(values=[x[0] for x in fetch])
    i.set("Poista käyttäjä")
    l.clear()
    for x in fetch:
        l.append(x[0])

def paivittaa_list_haku(kayttajat_list, box):
    """
    Päivitää listoja jotka näkyy kun hakee inputissa
    """
    # poistaa kaiken inputista, näin jotta käy yksitellen jokaisen läpi niin ei tuu erroria
    for _ in range(box.size()):
        box.delete(0)
    # lisää arvot uudestaan listaa jotta päivittyy
    for index, item in enumerate(kayttajat_list):
        box.insert(index, item)

def tayttaa_input(hae, box):
    """
    laittaa clikatun valuen inputtiin
    """
    # poistaa kaiken inputista
    hae.delete(0, END)
    # lisää klikatun arvon inputtiin
    hae.insert(0, box.get())

def filter_haku(haku, tuotteet):
    """
    kun kirjoittaa inputtiin hakee tietoa ja rajaa sillä jos sana/kirjain on jossain arvossa.
    saa parametreista arvot.
    """
    data = []
    for item in tuotteet:
        if haku in str(item).lower():
            data.append(item)
    return data

def lisaa_arvot(fetch, l):
    """
    lisää arvot listoihin
    """
    for x in fetch:
        l.append(x[0])

# Tehdään arvojen poistot
def kayttaja_poista(kayttajat_input, hae_kayttaja, button_kayttaja, text_vapa, hae_vapa, vapa_input, button_vapa, vapa_list_box, kayttajat_list_box, kayttajat_list):

    # tarkistaa kummasta ottaa arvon input vai valikosta 
    kayttaja_poista_input = kayttajat_input.get().split()
    if kayttaja_poista_input == "" or "Poista" in kayttaja_poista_input:
        kayttaja_poista_input = hae_kayttaja.get().split()
        # laitetaan labelit, inputit tms takasin paikalleen
        paikat([(kayttajat_input, {"x": 210, "y": 160}), (button_kayttaja, {"x": 210, "y": 190}), (text_vapa, {"x": 210, "y": 250}), (hae_vapa, {"x": 210, "y": 280}), (vapa_input, {"x": 210, "y": 310}), (button_vapa, {"x": 210, "y": 340})])
        paikat_unohtaa([vapa_list_box, kayttajat_list_box])
        kayttajat_input.set("Poista käyttäjä")
        hae_kayttaja.delete(0, END)

    # poistetaan käyttäjä ja siihen kuuluvat tiedot
    cursor.execute(f"SELECT id FROM kalastaja WHERE email='{kayttaja_poista_input[0]}'")
    kayttajat_id = cursor.fetchall()
    cursor.execute(f"SELECT id FROM tarppi WHERE kalastaja_id='{kayttajat_id[0][0]}'")
    tarppi_idt = cursor.fetchall()
    for c in tarppi_idt:
        cursor.execute(f"DELETE FROM kala WHERE tarppi_id='{c[0]}'")
    cursor.execute(f"DELETE FROM tarppi WHERE kalastaja_id='{kayttajat_id[0][0]}'")
    cursor.execute(f"DELETE FROM kalastaja WHERE email='{kayttaja_poista_input[0]}'")
    
    # tallettaa tapahtuneen tietokantaan
    connection.commit()

    # päivittää listat ja luettelot
    cursor.execute("SELECT email FROM kalastaja")
    kayttajat = cursor.fetchall()
    paivittaa(kayttajat, kayttajat_input, kayttajat_list)

def laji_poista(laji_input, hae_laji, button_laji, text_viehe, hae_viehe, viehe_input, button_viehe, viehe_list_box, laji_list_box, lajit_list):
    
    # tarkistaa kummasta ottaa arvon input vai valikosta 
    saa_laji_input = laji_input.get().split()
    if saa_laji_input == "" or "Poista" in saa_laji_input:
        saa_laji_input = hae_laji.get().split()
        # laitetaan labelit, inputit tms takasin paikalleen
        paikat([(laji_input, {"x": 590, "y": 160}), (button_laji, {"x": 590, "y": 190}), (text_viehe, {"x": 590, "y": 250}), (hae_viehe, {"x": 590, "y": 280}), (viehe_input, {"x": 590, "y": 310}), (button_viehe, {"x": 590, "y": 340})])                 
        paikat_unohtaa([viehe_list_box, laji_list_box])
        laji_input.set("Poista laji")
        hae_laji.delete(0, END)
    
    # ignooraa forekey ja poistaa tiedot
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")        
    cursor.execute(f"SELECT id FROM laji WHERE laji='{saa_laji_input[0]}'")
    laji_id = cursor.fetchall()
    cursor.execute(f"UPDATE kala set laji_id = NULL WHERE laji_id ='{laji_id[0][0]}'")        
    cursor.execute(f"DELETE FROM laji WHERE laji='{saa_laji_input[0]}'")        
    
    # tallettaa tapahtuneen tietokantaan
    connection.commit()
    
    # päivittää listat ja luettelot
    cursor.execute("SELECT laji FROM laji")
    lajit = cursor.fetchall()
    paivittaa(lajit, laji_input, lajit_list)

def vapa_poista(vapa_input, hae_vapa, button_vapa, vapa_list_box, vavat_list):
    # tarkistaa kummasta ottaa arvon input vai valikosta 
    saa_vapa_input = vapa_input.get().split()
    if saa_vapa_input == "" or "Poista" in saa_vapa_input:
        saa_vapa_input = hae_vapa.get().split()
        paikat([(vapa_input, {"x": 210, "y": 310}), (button_vapa, {"x": 210, "y": 340})])        
        paikat_unohtaa([vapa_list_box])
        vapa_input.set("Poista viehe")
        hae_vapa.delete(0, END)
    
    # ignooraa  forekey ja poistaa tiedot
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")        
    cursor.execute(f"SELECT id FROM vapa WHERE vapa ='{saa_vapa_input[0]}'")
    vapa_id = cursor.fetchall()
    cursor.execute(f"UPDATE tarppi set vapa_id = NULL WHERE vapa_id ='{vapa_id[0][0]}'") 
    cursor.execute(f"DELETE FROM vapa WHERE vapa='{saa_vapa_input[0]}'")        
    
    # tallettaa tapahtuneen tietokantaan
    connection.commit()
    
    # päivittää listat ja luettelot
    cursor.execute("SELECT vapa FROM vapa")
    vavat = cursor.fetchall()
    paivittaa(vavat, vapa_input, vavat_list)

def viehe_poista(viehe_input, hae_viehe, button_viehe, viehe_list_box, viehet_list):
    # tarkistaa kummasta ottaa arvon input vai valikosta 
    saa_viehe_input = viehe_input.get().split()
    if saa_viehe_input == "" or "Poista" in saa_viehe_input:
        saa_viehe_input = hae_viehe.get().split()
        paikat([(viehe_input, {"x": 590, "y": 310}), (button_viehe, {"x": 590, "y": 340})])
        paikat_unohtaa([viehe_list_box])
        viehe_input.set("Poista viehe")
        hae_viehe.delete(0, END)
    
    # ignooraa forekey ja poistaa tiedot
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")        
    cursor.execute(f"SELECT id FROM viehe WHERE viehe ='{saa_viehe_input[0]}'")
    viehe_id = cursor.fetchall()
    cursor.execute(f"UPDATE tarppi set viehe_id = NULL WHERE viehe_id ='{viehe_id[0][0]}'") 
    cursor.execute(f"DELETE FROM viehe WHERE viehe='{saa_viehe_input[0]}'")        
    
    # tallettaa tapahtuneen tietokantaan
    connection.commit()
    
    # päivittää listat ja luettelot
    cursor.execute("SELECT viehe FROM viehe")
    viehet = cursor.fetchall()
    paivittaa(viehet, viehe_input, viehet_list)
    
# ottaa input arvon ja päivittää listaa haun mukaan
def tarkistaa_input_kayttaja(hae_kayttaja, kayttajat_list_box, button_kayttaja, kayttajat_input, text_vapa, hae_vapa, vapa_input, button_vapa, vapa_list_box, kayttajat_list):
    
    # muokka kenttien ja nappin paikkoja sekä saa inputin
    hae_kayttaja_input = hae_kayttaja.get()
    paikat([(kayttajat_list_box, {"x": 210, "y": 165}), (button_kayttaja, {"x": 423, "y": 130})])
    paikat_unohtaa([kayttajat_input,text_vapa,hae_vapa, vapa_input,button_vapa,vapa_list_box])
    
    # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
    if hae_kayttaja_input == '':
        data_kayttaja = kayttajat_list
        paikat([(kayttajat_input, {"x": 210, "y": 160}), (button_kayttaja, {"x": 210, "y": 190}), (text_vapa, {"x": 210, "y": 250}), (hae_vapa, {"x": 210, "y": 280}), (vapa_input, {"x": 210, "y": 310}), (button_vapa, {"x": 210, "y": 340})])
        paikat_unohtaa([vapa_list_box,kayttajat_list_box])
        kayttajat_input.set("Poista käyttäjä")
        hae_kayttaja.delete(0, END)
    else:
        data_kayttaja = filter_haku(hae_kayttaja_input.lower(), kayttajat_list)
    
    # päivittää listaa joka näkyy kun hakee haun perusteella
    paivittaa_list_haku(data_kayttaja, kayttajat_list_box)
     
    
def tarkistaa_input_laji(hae_laji, laji_list_box, button_laji, laji_input, text_viehe, hae_viehe, viehe_input, button_viehe, viehe_list_box, lajit_list):
    
    # muokka kenttien ja nappin paikkoja sekä saa inputin
    laji_kayttaja_input = hae_laji.get()
    paikat([(laji_list_box, {"x": 590, "y": 165}), (button_laji, {"x": 803, "y": 130})])
    paikat_unohtaa([laji_input,text_viehe,hae_viehe, viehe_input,button_viehe,viehe_list_box])
    
    # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
    if laji_kayttaja_input == '':
        data_laji = lajit_list
        paikat([(laji_input, {"x": 590, "y": 160}), (button_laji, {"x": 590, "y": 190}), (text_viehe, {"x": 590, "y": 250}), (hae_viehe, {"x": 590, "y": 280}), (viehe_input, {"x": 590, "y": 310}), (button_viehe, {"x": 590, "y": 340})])
        paikat_unohtaa([viehe_list_box,laji_list_box])
        laji_input.set("Poista laji")
        hae_laji.delete(0, END)
    else:
        data_laji = filter_haku(laji_kayttaja_input.lower(), lajit_list)
    
    # päivittää listaa joka näkyy kun hakee haun perusteella
    paivittaa_list_haku(data_laji, laji_list_box)
    
def tarkistaa_input_viehe(hae_viehe, viehe_list_box, button_viehe, viehe_input, viehet_list):
    
    # muokka kenttien ja nappin paikkoja sekä saa inputin
    viehe_kayttaja_input = hae_viehe.get()
    paikat([(viehe_list_box, {"x": 590, "y": 310}), (button_viehe, {"x": 803, "y": 280})])
    paikat_unohtaa([viehe_input])
    
    # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
    if viehe_kayttaja_input == '':
        data_viehe = viehet_list
        paikat([(viehe_input, {"x": 590, "y": 310}), (button_viehe, {"x": 590, "y": 340})])
        paikat_unohtaa([viehe_list_box])
        viehe_input.set("Poista viehe")
        hae_viehe.delete(0, END)
    else:
        data_viehe = filter_haku(viehe_kayttaja_input.lower(), viehet_list)
    
    # päivittää listaa joka näkyy kun hakee haun perusteella
    paivittaa_list_haku(data_viehe, viehe_list_box)

def tarkistaa_input_vapa(hae_vapa, vapa_list_box, button_vapa, vapa_input, vavat_list):
    
    # muokka kenttien ja nappin paikkoja sekä saa inputin
    vapa_input_hae = hae_vapa.get()
    paikat([(vapa_list_box, {"x": 210, "y": 310}), (button_vapa, {"x": 423, "y": 280})])
    paikat_unohtaa([vapa_input])
    
    # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
    if vapa_input_hae == '':
        data_vapa = vavat_list
        paikat([(vapa_input, {"x": 210, "y": 310}), (button_vapa, {"x": 210, "y": 340})])
        paikat_unohtaa([vapa_list_box])
        vapa_input.set("Poista viehe")
        hae_vapa.delete(0, END)
    else:
        data_vapa = filter_haku(vapa_input_hae.lower(), vavat_list)
    
    # päivittää listaa joka näkyy kun hakee haun perusteella
    paivittaa_list_haku(data_vapa, vapa_list_box)

def admin_window(root):
    """
    luodaan admin ikkuna ja siihen buttonit, labelit, luettelot ja tekstit.
    lambda: sallii lähettää parametreja kun esim buttoni kutsuu functiota.
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
    """
    luodaan frame, jotta kaikki admin_window buttonit,
    label tms täbin sisällä pysyvät aina samassa paikassa
    """
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
    hae_kayttaja = ctk.CTkEntry(container, textvariable=hae_string_var,font=('calibre',12,'normal'), width=200)
    hae_kayttaja.place(x=210, y=130)        

    # luettelo boxsi
    kayttajat_input = ctk.CTkComboBox(container, values=[x[0] for x in kayttajat], font=('calibre',15))
    kayttajat_input.set("Poista käyttäjä")
    kayttajat_input.place(x=210, y=160)

    # button
    button_kayttaja = ctk.CTkButton(master=container ,text="Poista käyttäjä", command=lambda: kayttaja_poista(
        kayttajat_input,
        hae_kayttaja,
        button_kayttaja,
        text_vapa,
        hae_vapa,
        vapa_input,
        button_vapa,
        vapa_list_box,
        kayttajat_list_box,
        kayttajat_list
    ))
    button_kayttaja.place(x=210, y=190)

    # kuuntelee jos kayttajat_list_box arvo klikattu
    kayttajat_list_box.bind("<Button-1>", lambda e: tayttaa_input(hae_kayttaja, kayttajat_list_box))
    # päivittää kayttajat_list_box
    paivittaa_list_haku(kayttajat_list, kayttajat_list_box)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_kayttaja.bind('<KeyRelease>', lambda e: tarkistaa_input_kayttaja(
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
    hae_laji = ctk.CTkEntry(container, textvariable=laji_hae_string_var, font=('calibre',12,'normal'), width=200)
    hae_laji.place(x=590, y=130) 

    # luettelo boxsi
    laji_input = ctk.CTkComboBox(container, values=[x[0] for x in lajit], font=('calibre',15))
    laji_input.set("Poista laji")
    laji_input.place(x=590, y=160)

    # button
    button_laji = ctk.CTkButton(master=container ,text="Poista laji", command=lambda: laji_poista(
        laji_input,
        hae_laji,
        button_laji,
        text_viehe,
        hae_viehe,
        viehe_input,
        button_viehe,
        viehe_list_box,
        laji_list_box,
        lajit_list
    ))
    button_laji.place(x=590, y=190)

    # kuuntelee jos laji_list_box arvo klikattu
    laji_list_box.bind("<Button-1>", lambda e: tayttaa_input(hae_laji, laji_list_box))
    # päivittää laji_list_box
    paivittaa_list_haku(lajit_list, laji_list_box)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_laji.bind('<KeyRelease>', lambda e: tarkistaa_input_laji(
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
    hae_vapa = ctk.CTkEntry(container, textvariable=vapa_hae_string_var, font=('calibre',12,'normal'), width=200)
    hae_vapa.place(x=210, y=280) 

    # luettelo boxsi
    vapa_input = ctk.CTkComboBox(container, values=[x[0] for x in vavat], font=('calibre',15))
    vapa_input.set("Poista vapa")
    vapa_input.place(x=210, y=310)
    
    # button
    button_vapa = ctk.CTkButton(master=container ,text="Poista vapa", command=lambda: vapa_poista(
        vapa_input,
        hae_vapa,
        button_vapa,
        vapa_list_box,
        vavat_list
    ))
    button_vapa.place(x=210, y=340)

    # kuuntelee jos vapa_list_box arvo klikattu
    vapa_list_box.bind("<Button-1>", lambda e: tayttaa_input(hae_vapa, vapa_list_box))
    # päivittää vapa_list_box
    paivittaa_list_haku(vavat_list, vapa_list_box)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_vapa.bind('<KeyRelease>', lambda e: tarkistaa_input_vapa(
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
    hae_viehe = ctk.CTkEntry(container, textvariable=viehe_hae_string_var, font=('calibre',12,'normal'), width=200)
    hae_viehe.place(x=590, y=280) 

    # luettelo boxsi
    viehe_input = ctk.CTkComboBox(container, values=[x[0] for x in viehet], font=('calibre',15))
    viehe_input.set("Poista viehe")
    viehe_input.place(x=590, y=310)
    
    # button
    button_viehe = ctk.CTkButton(master=container ,text="Poista viehe", command=lambda: viehe_poista(
        viehe_input,
        hae_viehe,
        button_viehe,
        viehe_list_box,
        viehet_list
    ))
    button_viehe.place(x=590, y=340)
  
    # kuuntelee jos viehe_list_box arvo klikattu
    viehe_list_box.bind("<Button-1>", lambda e: tayttaa_input(hae_viehe, viehe_list_box))
    # päivittää viehe_list_box
    paivittaa_list_haku(viehet_list, viehe_list_box)
    # kuuntelee jos inputtiin kirjoitetaan
    hae_viehe.bind('<KeyRelease>', lambda e: tarkistaa_input_viehe(
        hae_viehe,
        viehe_list_box,
        button_viehe,
        viehe_input,
        viehet_list
    ))

    # jos painaa x:sää sulkee ikkunan
    def close():
        root.destroy()
    window.protocol("WM_DELETE_WINDOW", close)
