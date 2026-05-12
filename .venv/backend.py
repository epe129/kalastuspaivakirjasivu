# jatka loppuun että voi poistaa laji tms 
import customtkinter as ctk
import pymysql, dbinfo, datetime 
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import *
from tkcalendar import DateEntry
import bcrypt

# otetaan db tiedot python tiedostosta
USER = dbinfo.data["USER"]
PASSWORD = dbinfo.data["PASSWORD"]
DBNIMI = dbinfo.data["DBNIMI"]
PORT = dbinfo.data["PORT"]
HOST = dbinfo.data["HOST"]


# yhteys tietokantaan
connection = pymysql.connect(host=HOST, port=PORT, user=USER, password=PASSWORD, database=DBNIMI)
cursor = connection.cursor()

ctk.set_appearance_mode("System") 

# luodaan ikkuna
root = ctk.CTk()
root.resizable(width=False, height=False)
root.geometry("600x600")
root.title("Admin")

def admin_window():
    ctk.set_appearance_mode("System") 
    admin_window = ctk.CTk()
    admin_window.geometry("1000x600")  
    admin_window.resizable(width=False, height=False)
    admin_window.title("Admin")
    window_width = admin_window.winfo_width()

    def kayttaja_poista():
        kayttaja_poista = kayttajat_input.get().split()
        if kayttaja_poista == "" or "Poista" in kayttaja_poista:
            kayttaja_poista = hae_kayttaja.get().split()
            kayttajat_input.place(x=10, y=160)  
            button_kayttaja.place(x=10, y=190)
            my_list.place(x=-10, y=-190)
            kayttajat_input.set("Poista käyttäjä")
            hae_kayttaja.delete(0, END)

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
    
    def laji_poista():
        saa_laji_input = laji_input.get().split()
        print(saa_laji_input)
        # cursor.execute(f"")        
        # tallettaa tapahtuneen tietokantaan
        # connection.commit()

    def vapa_poista():
        saa_vapa_input = vapa_input.get().split()
        print(saa_vapa_input)
        # cursor.execute(f"")        
        # tallettaa tapahtuneen tietokantaan
        # connection.commit()

    def viehe_poista():
        saa_viehe_input = viehe_input.get().split()
        print(saa_viehe_input)
        # cursor.execute(f"")        
        # tallettaa tapahtuneen tietokantaan
        # connection.commit()

    # oteteaan data tietokannasat
    kayttajat_list = []
    cursor.execute(f"SELECT email FROM kalastaja")
    kayttajat = cursor.fetchall()
    for x in kayttajat:
        kayttajat_list.append(x[0])
    cursor.execute(f"SELECT laji FROM laji")
    lajit = cursor.fetchall()
    cursor.execute(f"SELECT vapa FROM vapa")
    vavat = cursor.fetchall()
    cursor.execute(f"SELECT viehe FROM viehe")
    viehet = cursor.fetchall()

    text_admin = ctk.CTkLabel(admin_window, text="Admin", font=('calibre',40))
    text_admin.place(x=450, y=25)

    my_list = Listbox(admin_window, width=50)

    # käyttäjän poisto
    # otsikko
    text_kayttaja = ctk.CTkLabel(admin_window, text="Poista käyttäjä:", font=('calibre',20))
    text_kayttaja.place(x=10, y=100)

    hae_string_var = StringVar()
    hae_kayttaja = tk.Entry(admin_window, textvariable=hae_string_var, font=('calibre',12,'normal'), width=25)
    hae_kayttaja.place(x=10, y=130)        
    # päivitää listaa
    def update(data):
        my_list.delete(0, END)
        for item in data:
            my_list.insert(END, item)

    # laittaa clikatun valuen inputtiin
    def fillout(e):
        # poistaa kaiken inputista
        hae_kayttaja.delete(0, END)
        # lisää klikatun arvon inputtiin
        hae_kayttaja.insert(0, my_list.get(ANCHOR))

    # entery boxin ja päivittää listaa haun mukaan
    def check(event):
        # muokka kenttien ja nappin paikkoja
        my_list.place(x=10, y=165)
        kayttajat_input.place(x=-10, y=-165)
        button_kayttaja.place(x=243, y=128)

        hae = hae_kayttaja.get()
        if hae == '':
            data = kayttajat_list
        else:
            data = []
            for item in kayttajat_list:
                if hae.lower() in item.lower():
                    data.append(item)
        update(data)

    # kuuntelee jos hiiren mouse 1 on painettu
    my_list.bind("<Button-1>", fillout)
    update(kayttajat_list)    
    # kuuntelee jos inputtiin kirjoitetaan
    hae_kayttaja.bind('<Key>', check)
    
    # luettelo boxsi
    kayttajat_input = ctk.CTkComboBox(admin_window, values=[x[0] for x in kayttajat], font=('calibre',15))
    kayttajat_input.set("Poista käyttäjä")
    kayttajat_input.place(x=10, y=160)
    # button
    button_kayttaja = ctk.CTkButton(master=admin_window ,text="Poista käyttäjä", command=kayttaja_poista)
    button_kayttaja.place(x=10, y=190)

    # laji poisto
    # otsikko
    text_laji = ctk.CTkLabel(admin_window, text="Poista laji:", font=('calibre',20))
    text_laji.place(x=390, y=100)
    # luettelo boxsi
    laji_input = ctk.CTkComboBox(admin_window, values=[x[0] for x in lajit], font=('calibre',15))
    laji_input.set("Poista laji")
    laji_input.place(x=390, y=130)
    # button
    button_laji = ctk.CTkButton(master=admin_window ,text="Lähetä", command=laji_poista)
    button_laji.place(x=390, y=160)

    # vapa poisto
    # otsikko
    text_vapa = ctk.CTkLabel(admin_window, text="Poista vapa:", font=('calibre',20))
    text_vapa.place(x=555, y=100)
    # luettelo boxsi
    vapa_input = ctk.CTkComboBox(admin_window, values=[x[0] for x in vavat], font=('calibre',15))
    vapa_input.set("Poista vapa")
    vapa_input.place(x=555, y=130)
    # button
    button_vapa = ctk.CTkButton(master=admin_window ,text="Lähetä", command=vapa_poista)
    button_vapa.place(x=555, y=160)

    # viehe poisto
    # otsikko
    text_viehe = ctk.CTkLabel(admin_window, text="Poista viehe:", font=('calibre',20))
    text_viehe.place(x=720, y=100)
    # luettelo boxsi
    viehe_input = ctk.CTkComboBox(admin_window, values=[x[0] for x in viehet], font=('calibre',15))
    viehe_input.set("Poista viehe")
    viehe_input.place(x=720, y=130)
    # button
    button_viehe = ctk.CTkButton(master=admin_window ,text="Lähetä", command=viehe_poista)
    button_viehe.place(x=720, y=160)

    # jos painaa x:sää sulkee ikkunan
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
        password = username = "admin"
        
        # tarkistaa onko salasana ja käyttäjänimi oikein
        # ei saa oikeasti tehäd näin jos olisi tuotannossa
        if username == dbinfo.data["admin_username"] and bcrypt.checkpw(password.encode("utf-8"), dbinfo.data["admin_password"]):
            root.withdraw()
            admin_window()
        else:
            text.place(x=window_width + 20, y=170)
            my_string_var.set("Salasana tai käyttäjänimi on väärin")
    except Exception as e:
        text.place(x=window_width + 70, y=170)
        my_string_var.set("Jokin meni vikaan")
        print(e)
    
# saa näytön leveyden
window_width = root.winfo_width()
# lasketaan x(leveys suunta) coordinaatiot keskelle sivua
x = (window_width)
z = (window_width)

# luodaan inpu teille tyyppi
username_var=tk.StringVar()
password_var=tk.StringVar()
my_string_var = StringVar()

l = ctk.CTkLabel(root, text = "Log in", font=('calibre',25,'bold'))
l.place(x=x + 100, y=75)

# name input
username = ctk.CTkLabel(root, text="Name:", font=('calibre',15))
username_input = tk.Entry(root, textvariable=username_var, font=('calibre',12,'normal'), width=25)
username.place(x=window_width - 23, y=115)
username_input.place(x=x + 25, y=115)

# password input
password = ctk.CTkLabel(root, text="Password:", font=('calibre',15))
password_input = tk.Entry(root, textvariable=password_var, font=('calibre',12,'normal'), show="*", width=25)
password.place(x=window_width - 50, y=145)
password_input.place(x=x + 25, y=145)

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

# def luettelo():
#     # kalalaji luettelo
#     global luettelo_lajit
#     luettelo_lajit = []
#     cursor.execute("SELECT laji FROM laji")
#     lajit_tulos = cursor.fetchall()
#     for x in lajit_tulos:
#         res = ' '.join(x)
#         luettelo_lajit.append(res)
#     luettelo_lajit.append("muu")
# luettelo()

# def get_input():
#     try:
#         # saadaan inputit
#         nimi = nimi_input.get()
#         laji = laji_input.get()
#         saatu_aika = aika.get_date()
#         paikka = paikka_input.get()
#         viehe = viehe_input.get()
#         vapa = vapa_input.get()
#         x = datetime.datetime.now()
#         nyky_aika = x.strftime("%Y-%m-%d")
#         # tarkistaa pituus ja paino ovat lukuja
#         try:
#             pituus = float(pituus_input.get())
#             paino = float(paino_input.get())
#         except:
#             # asettaa tekstin 
#             text.place(x=window_width + 350, y=425)
#             my_string_var.set("Pituus ja paino kohtiin pitää laittaa luku")
#             return
#         # tarkistaa ettei päivämäärä ole nyky aikaa suurempi
#         if str(saatu_aika) > str(nyky_aika):
#             text.place(x=window_width + 325, y=425)
#             my_string_var.set("Et voi laitta nykyaikaa suurempaa aikaa")
#             return
#         # tarkistaa ettei arvot ole tyhjiä tai jos on arvoja jotka ei kelpaa
#         if nimi == "" or pituus == "" or paino == "" or paino == "0" or pituus == "0" or laji == "Valitse kalalaji" or laji == "" or paikka == "" or viehe == "" or vapa == "":
#             text.place(x=window_width + 335, y=425)
#             my_string_var.set("Et täyttänyt kaikkia kohtia tai valinnut lajia")
#             return   
#         # tarkistaa että kirjaimia ei ole yli 24 merkki
#         if len(nimi) > 24 or len(laji) > 24 or len(viehe) > 24 or len(paikka) > 24 or len(vapa) > 24:
#             text.place(x=window_width + 370, y=425)
#             my_string_var.set("Maksimi merkkien määrä on 24")
#             return
#         # tarkistaa että kirjaimia ei ole yli 4 merkki
#         if len(str(pituus)) > 6 or len(str(paino)) > 6:
#             text.place(x=window_width + 300, y=425)
#             my_string_var.set("Painon ja pituuden maksimi merkkien määrä on 4")
#             return
#         # lähettää tiedot tietokantaan  
#         cursor.execute(f"SELECT * FROM kalastaja WHERE nimi ='{nimi}'")
#         select_nimi = cursor.fetchall()
#         print(len(select_nimi))
#         if len(select_nimi) == 0:
#             # lähettää datan tietokantaan
#             cursor.execute(f'INSERT INTO kalastaja (nimi) VALUES ("{nimi}")')        
#             # saa aina edellisen taulun id:n
#             kalastaja_id = cursor.lastrowid
#         else:
#             kalastaja_id = select_nimi[0][0]
        
#         cursor.execute(f'INSERT INTO viehe (viehe) VALUES ("{viehe}")')
#         viehe_id = cursor.lastrowid
#         cursor.execute(f'INSERT INTO vapa (vapa) VALUES ("{vapa}")')
#         vapa_id = cursor.lastrowid
        
#         cursor.execute(f"SELECT * FROM laji WHERE laji ='{laji}'")
#         select_laji = cursor.fetchall()
#         laji_id = select_laji[0][0]
        
#         cursor.execute(f'INSERT INTO tarppi (aika, kalastaja_id, viehe_id, vapa_id, paikka) VALUES ("{saatu_aika}", "{kalastaja_id}", "{viehe_id}", "{vapa_id}", "{paikka}")')
#         tarppi_id = cursor.lastrowid
#         cursor.execute(f'INSERT INTO kala (tarppi_id, pituus, paino, laji_id) VALUES ("{tarppi_id}", "{pituus}", "{paino}", "{laji_id}")')
#         # tallettaa tapahtuneen tietokantaan
#         connection.commit()
#         # asettaa tekstin 
#         text.place(x=window_width + 400, y=425)
#         my_string_var.set("Tiedot lisättiin onnistuneesti")
#     except:
#         text.place(x=window_width + 425, y=425)
#         my_string_var.set("Jokin meni vikaan")
#     tyhjenna_inputit()

# # saa näytön leveyden
# window_width = root.winfo_width()
# # lasketaan x(leveys suunta) coordinaatiot keskelle sivua
# x = (window_width + 400)
# z = (window_width + 400)
# nimi_paikka = (window_width + 350)
# pituus_paikka = (window_width + 295)
# paino_paikka = (window_width + 305)
# laji_paikka = (window_width + 265)
# aika_paikka = (window_width + 350)
# paikka_paikka = (window_width + 330)
# viehe_paikka = (window_width + 340)
# vapa_paikka = (window_width + 340)
# button_paikka = (window_width + 565)
# laji_muu_paikka = (window_width + 315)

# # luodaan teksti kenttä jossa teksti voi muuttua
# my_string_var = StringVar()
# my_string_var.set("")
# text = tk.Label(root, textvariable=my_string_var, font=('calibre',15))
# text.place(x=window_width + 350, y=425)

# # otsikko
# l = tk.Label(root, text = "Kalastustiedot", font=('calibre',20,'bold'))
# l.place(x=x, y=25)

# # luodaan inpu teille tyyppi
# nimi_var=tk.StringVar()
# pituus_var=tk.IntVar()
# paino_var=tk.DoubleVar()
# laji_var=tk.StringVar()
# aika_var=tk.StringVar()
# paikka_var=tk.StringVar()
# viehe_var=tk.StringVar()
# vapa_var=tk.StringVar()

# # luodaan inputit ja labelit
# nimi = tk.Label(root, text="Nimi:", font=('calibre',15))
# nimi_input = tk.Entry(root, textvariable=nimi_var, font=('calibre',15,'normal'), width=25)
# nimi.place(x=nimi_paikka, y=70)
# nimi_input.place(x=x, y=70)

# laji = tk.Label(root, text="Valitse kalalaji:", font=('calibre',15))
# laji.place(x=laji_paikka, y=110)

# laji_input = ttk.Combobox(root, values=luettelo_lajit, font=('calibre',15), textvariable=laji_var, state="readonly")
# laji_input.set("Valitse kalalaji")
# laji_input.place(x=x, y=110)
# # jos laitaa muu arvon, avaa ikkunan johon voi syöttää arvon
# def muu():
#     uusi_ikkuna = Toplevel(root)  
#     uusi_ikkuna.title("Uusi kalalaji")
#     uusi_ikkuna.geometry("450x250")  
#     uusi_ikkuna.resizable(width=False, height=False)
#     window_width = uusi_ikkuna.winfo_width()
    
#     def get_input():
#         try:
#             laji_text = laji_input_muu.get()
#         except:
#             pass
#         # tarkistaa ettei ole tyhjä
#         if laji_text == "": 
#             # asettaa tekstin
#             text_var.set("Annoit tyhjän arvon")
#             text.place(x=window_width+140, y=170)
#             return
#         try:
#             id = 0
#             cursor.execute(f"SELECT * FROM laji WHERE laji ='{laji_text}'")
#             laji_tarkistus = cursor.fetchall()

#             if len(laji_tarkistus) == 0:
#                 cursor.execute(f"SELECT * FROM laji")
#                 laji_id = cursor.fetchall()
#                 id = len(laji_id) + 1
#                 cursor.execute(f'INSERT INTO laji (id, laji) VALUES ("{id}", "{laji_text}")')
#                 # tallettaa tapahtuneen tietokantaan
#                 connection.commit()
#                 text_var.set("Uusi laji lisättiin onnistuneesti tietokantaan")
#                 text.place(x=window_width+40, y=170)
#                 # päivitää listaa
#                 laji_input_muu.delete(0, END)
#                 laji_input.set("Valitse kalalaji")
#                 luettelo_lajit.remove("muu")
#                 luettelo_lajit.append(laji_text)
#                 luettelo_lajit.append("muu")
#                 laji_input['values'] = luettelo_lajit
#             else:
#                 laji_input.set("Valitse kalalaji")
#                 text_var.set("Laji on jo tietokannassa")
#                 text.place(x=window_width+110, y=170)
#         except ValueError as e:
#             print(e)

#     text_var = StringVar()
#     laji_var_muu=tk.StringVar()
#     text_var.set("")
#     # luodaan inputit ja labelit
#     text = tk.Label(uusi_ikkuna, textvariable = text_var, font=('calibre',15))
#     text.place(x=x+10, y=100)
#     laji_muu_text = tk.Label(uusi_ikkuna, text="Anna uusi kalalaji:", font=('calibre',15))
#     laji_input_muu = tk.Entry(uusi_ikkuna, textvariable=laji_var_muu, font=('calibre',15,'normal'), width=25)
#     laji_input_muu.place(x=window_width + 90, y=70)
#     laji_muu_text.place(x=window_width + 140, y=30)
#     button = ttk.Button(uusi_ikkuna, text="Lähetä", command=get_input, style='TButton', cursor="hand2")
#     button.place(x=window_width + 155, y=120)

# def saa_arvon(*args):
#     # jos arvo on muu laittaa input johon käyttäjä voi itse kirjoittaa lajin
#     if str(laji_var.get()) == "muu":
#         muu()

# # katsoo mikä arvo on valittu luettelosta
# laji_var.trace_add('write', saa_arvon)

# pituus = tk.Label(root, text="Pituus(cm):", font=('calibre',15))
# pituus_input = tk.Entry(root, textvariable=pituus_var, font=('calibre',15,'normal'), width=25)
# pituus.place(x=pituus_paikka, y=150)
# pituus_input.place(x=x, y=150)
    
# paino = tk.Label(root, text="Paino(kg):", font=('calibre',15))
# paino_input = tk.Entry(root, textvariable=paino_var, font=('calibre',15,'normal'), width=25)
# paino.place(x=paino_paikka, y=190)
# paino_input.place(x=x, y=190)

# paikka = tk.Label(root, text="Paikka:", font=('calibre',15))
# paikka_input = tk.Entry(root, textvariable=paikka_var, font=('calibre',15,'normal'), width=25)
# paikka.place(x=paikka_paikka, y=230)
# paikka_input.place(x=x, y=230)

# aika_text = tk.Label(root, text="Aika:", font=('calibre',15))
# aika = DateEntry(root, width=12, background="darkblue", foreground="white", borderwidth=2, font=('calibre',15,'normal'), date_pattern="dd.mm.yyyy")
# aika_input = tk.Entry(root, textvariable=aika_var, font=('calibre',15,'normal'))
# aika_text.place(x=aika_paikka, y=270)
# aika.place(x=x, y=270)

# viehe = tk.Label(root, text="Viehe:", font=('calibre',15))
# viehe_input = tk.Entry(root, textvariable=viehe_var, font=('calibre',15,'normal'), width=25)
# viehe.place(x=viehe_paikka, y=310)
# viehe_input.place(x=x, y=310)

# vapa = tk.Label(root, text="Vapa:", font=('calibre',15))
# vapa_input = tk.Entry(root, textvariable=vapa_var, font=('calibre',15,'normal'), width=25)
# vapa.place(x=vapa_paikka, y=350)
# vapa_input.place(x=x, y=350)

# def tyhjenna_inputit():
#    # tyhjen tää inputit kun arvot lähetetty
#    nimi_input.delete(0, END)
#    pituus_input.delete(0, END)
#    paino_input.delete(0, END)
#    laji_input.set("Valitse kalalaji")
#    paikka_input.delete(0, END)
#    viehe_input.delete(0, END)
#    vapa_input.delete(0, END)
   
   
# # luodaan tyylit buttoniin ja luodaan buttoni
# style = ttk.Style()
# style.configure('TButton', font = ('calibri', 15, 'bold'), borderwidth = '4')
# button = ttk.Button(text="Lähetä", command=get_input, style='TButton', cursor="hand2")
# button.place(x=button_paikka, y=390)

# # voit vaihtaa kuinka nopeaa dia esitys menee sivulla
# def intecraatio():
#     # luodaa uusi ikkuna
#     uusi_ikkuna = Toplevel(root)  
#     uusi_ikkuna.title("Diaesityksen nopeus")
#     uusi_ikkuna.geometry("450x250")  
#     uusi_ikkuna.resizable(width=False, height=False)
#     window_width = uusi_ikkuna.winfo_width()
#     # asetetaan elementtien sijainnit leveys suunnassa
#     x = (window_width)
#     nopeus_x = (x + 5)
#     nopeus_input_x = (x + 90)
#     button_x = (x + 135)
#     def get_input():
#         s = 0
#         # tarkistaa että nopeus on int
#         try:
#             nopeus = int(nopeus_input.get())
#         except:
#             text.place(x=x+10, y=100)
#             # asettaa tekstin
#             text_var.set("Annoit kirjaimia, pitää olla numero väliltä 1-20")
#             return
#         # tarkistaa ettei ole tyhjä
#         if nopeus == "": 
#             # asettaa tekstin
#             text_var.set("Annoit tyhjän arvon")
#             text.place(x=x+110, y=100)
#             return
#         # laskee millisekunteiksi
#         s = int(nopeus) * 1000
#         # tarkistaa että nopeus on oikealla arvo alueeella
#         if s > 20000 or s < 1000:
#             # asettaa tekstin
#             text.place(x=x+10, y=100)
#             text_var.set("Annoit joko liian suuren tai liian pienen luvun")
#             return
#         cursor.execute(f'INSERT INTO integraatiot (diaNopeus) VALUES ("{s}")')            
#         # tallettaa tapahtuneen tietokantaan
#         connection.commit()
#         text_var.set("Vaihtui onnistuneesti")
#         text.place(x=x+110, y=100)
#         nopeus_input.delete(0, END)

#     text_var = StringVar()
#     text_var.set("")
#     # luodaan inputit ja labelit
#     text = tk.Label(uusi_ikkuna, textvariable = text_var, font=('calibre',15))
#     text.place(x=x+10, y=100)
#     nopeus_var = tk.IntVar()
#     nopeus = tk.Label(uusi_ikkuna, text="Anna diaesityksen nopeus sekunteina(1-20):", font=('calibre',15))
#     nopeus_input = tk.Entry(uusi_ikkuna, textvariable=nopeus_var, font=('calibre',15,'normal'))
#     nopeus.place(x=nopeus_x, y=30) 
#     nopeus_input.place(x=nopeus_input_x, y=70)
#     button = ttk.Button(uusi_ikkuna, text="Lähetä", command=get_input, style='TButton', cursor="hand2")
#     button.place(x=button_x, y=140)
# # luodaan buttoniin tyyli ja buttoni
# style.configure('W.TButton', font = ('calibri', 17, 'bold'), borderwidth = '4')
# button = ttk.Button(text="Vaihda diaesityksen nopeutta", command=intecraatio, style='W.TButton', cursor="hand2")
# button.place(x=5, y=5)