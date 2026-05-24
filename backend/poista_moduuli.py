"""
Moduuli tiedosto arvojen poisto fucntioille. 
"""
import admin_window
from tkinter import END

# Tehdään arvojen poistot
def kayttaja_poista(kayttajat_input, hae_kayttaja, button_kayttaja, text_vapa, hae_vapa, vapa_input, button_vapa, vapa_list_box, kayttajat_list_box, kayttajat_list, cursor, connection):

    # tarkistaa kummasta ottaa arvon input vai valikosta 
    kayttaja_poista_input = kayttajat_input.get().split()
    if kayttaja_poista_input == "" or "Poista" in kayttaja_poista_input:
        kayttaja_poista_input = hae_kayttaja.get().split()
        # laitetaan labelit, inputit tms takasin paikalleen
        admin_window.paikat([(kayttajat_input, {"x": 210, "y": 160}), (button_kayttaja, {"x": 210, "y": 190}), (text_vapa, {"x": 210, "y": 250}), (hae_vapa, {"x": 210, "y": 280}), (vapa_input, {"x": 210, "y": 310}), (button_vapa, {"x": 210, "y": 340})])
        admin_window.paikat_unohtaa([vapa_list_box, kayttajat_list_box])
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
    
    admin_window.paivittaa(kayttajat, kayttajat_input, kayttajat_list)

def laji_poista(laji_input, hae_laji, button_laji, text_viehe, hae_viehe, viehe_input, button_viehe, viehe_list_box, laji_list_box, lajit_list, cursor, connection):
    
    # tarkistaa kummasta ottaa arvon input vai valikosta 
    saa_laji_input = laji_input.get().split()
    if saa_laji_input == "" or "Poista" in saa_laji_input:
        saa_laji_input = hae_laji.get().split()
        # laitetaan labelit, inputit tms takasin paikalleen
        admin_window.paikat([(laji_input, {"x": 590, "y": 160}), (button_laji, {"x": 590, "y": 190}), (text_viehe, {"x": 590, "y": 250}), (hae_viehe, {"x": 590, "y": 280}), (viehe_input, {"x": 590, "y": 310}), (button_viehe, {"x": 590, "y": 340})])                 
        admin_window.paikat_unohtaa([viehe_list_box, laji_list_box])
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

    admin_window.paivittaa(lajit, laji_input, lajit_list)

def vapa_poista(vapa_input, hae_vapa, button_vapa, vapa_list_box, vavat_list, cursor, connection):
    # tarkistaa kummasta ottaa arvon input vai valikosta 
    saa_vapa_input = vapa_input.get().split()
    if saa_vapa_input == "" or "Poista" in saa_vapa_input:
        saa_vapa_input = hae_vapa.get().split()
        admin_window.paikat([(vapa_input, {"x": 210, "y": 310}), (button_vapa, {"x": 210, "y": 340})])        
        admin_window.paikat_unohtaa([vapa_list_box])
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
    admin_window.paivittaa(vavat, vapa_input, vavat_list)

def viehe_poista(viehe_input, hae_viehe, button_viehe, viehe_list_box, viehet_list, cursor, connection):
    # tarkistaa kummasta ottaa arvon input vai valikosta 
    saa_viehe_input = viehe_input.get().split()
    if saa_viehe_input == "" or "Poista" in saa_viehe_input:
        saa_viehe_input = hae_viehe.get().split()
        admin_window.paikat([(viehe_input, {"x": 590, "y": 310}), (button_viehe, {"x": 590, "y": 340})])
        admin_window.paikat_unohtaa([viehe_list_box])
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
    admin_window.paivittaa(viehet, viehe_input, viehet_list)
