"""
Moduuli tiedosto functiolle joka ottaa input arvon ja
päivittää CTkListbox(lista joka näkyy kun hakee inputilla) haun mukaan.
"""
from tkinter import END
import admin_window

def tarkistaa_input(
                    hae,
                    list_,
                    input_,
                    list_box,
                    paikat_1,
                    paikat_2,
                    paikat_3,
                    paikat_4
                    ):
    """
    Saadaan parametreistä input arvo jonka 
    mukaan päivitetään CTkListbox(lista joka näkyy kun hakee inputilla).
    """
    # muokkaa kenttien ja nappin paikkoja sekä saa inputin
    hae_input = hae.get()
    admin_window.paikat(paikat_1)
    admin_window.paikat_unohtaa(paikat_2)
    # jos haku kenttä on tyhjä laittaa buttonit ja muut inputit/tekstit takaisin paikoilleen 
    if hae_input == '':
        data = list_
        admin_window.paikat(paikat_3)
        admin_window.paikat_unohtaa(paikat_4)
        input_.set("Poista käyttäjä")
        hae.delete(0, END)
    else:
        data = []
        for item in list_:
            if hae_input.lower() in str(item).lower():
                data.append(item)
    # päivittää listaa joka näkyy kun hakee inputilla
    admin_window.paivittaa_list_haku(data, list_box)
