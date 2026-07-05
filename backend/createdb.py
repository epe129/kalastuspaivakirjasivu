"""
Luodaan tietokanta ja taulut.
pymysql avulla yhdistää tietokantaan.
dbinfosta saa databasen yhdistämiseen tarvittavat tiedot.
"""
import pymysql
import dbinfo

def databasen_luonti():
    """
    Luodaan itse tietokanta jos ei ole olemassa.
    """
    connection_luonti = pymysql.connect(host=dbinfo.data["HOST"], port=dbinfo.data["PORT"],
    user=dbinfo.data["USER"], password=dbinfo.data["PASSWORD"])
    cursor_luonti = connection_luonti.cursor()
    cursor_luonti.execute("CREATE DATABASE IF NOT EXISTS kalastustietosivu2")

# luodaan yhteys
try:
    databasen_luonti()
    connection = pymysql.connect(host=dbinfo.data["HOST"], port=dbinfo.data["PORT"],
    user=dbinfo.data["USER"], password=dbinfo.data["PASSWORD"], database=dbinfo.data["DBNIMI"])
    cursor = connection.cursor()
except ImportError:
    print("Yhteyden luominen epäonnistui")

def db():
    """
    luodaan tietokannan taulut sekä lisätään laji, vapa ja viehe arvot.
    """
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS admin "
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE, username VARCHAR(45) NOT NULL, pword VARCHAR(255) NOT NULL);")
        cursor.execute("CREATE TABLE IF NOT EXISTS KALASTAJA "
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL UNIQUE, nimi VARCHAR(45) NOT NULL, email VARCHAR(45) NOT NULL UNIQUE, pword VARCHAR(255) NOT NULL);")
        cursor.execute("CREATE TABLE IF NOT EXISTS VIEHE "
        "( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL  UNIQUE, viehe TEXT NOT NULL);")
        cursor.execute("CREATE TABLE IF NOT EXISTS VAPA"
        " ( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL  UNIQUE, vapa TEXT NOT NULL);")
        cursor.execute("CREATE TABLE IF NOT EXISTS LAJI"
        " ( id INT AUTO_INCREMENT PRIMARY KEY NOT NULL  UNIQUE, laji TEXT NOT NULL UNIQUE);")
        cursor.execute("CREATE TABLE IF NOT EXISTS TARPPI"
        " ( id INT AUTO_INCREMENT NOT NULL  UNIQUE, aika DATETIME NOT NULL, kalastaja_id INT NOT NULL, viehe_id INT NOT NULL, vapa_id INT NOT NULL, paikka TEXT, FOREIGN KEY (kalastaja_id) REFERENCES KALASTAJA(id), FOREIGN KEY (viehe_id) REFERENCES VIEHE(id), FOREIGN KEY (vapa_id) REFERENCES VAPA(id), PRIMARY KEY (id, kalastaja_id, viehe_id, vapa_id));")
        cursor.execute("CREATE TABLE IF NOT EXISTS KALA"
        " ( id INT AUTO_INCREMENT NOT NULL  UNIQUE, tarppi_id INT NOT NULL, pituus FLOAT, paino FLOAT, laji_id INT NOT NULL, kuva VARCHAR(255), FOREIGN KEY (tarppi_id) REFERENCES TARPPI(id), FOREIGN KEY (laji_id) REFERENCES LAJI(id), PRIMARY KEY (id, tarppi_id));")
        lajit = ["ahven", "harjus", "hauki", "jokirapu", "kiiski", "kirjolohi", "kolmipiikki",
                "kuha","kuore", "lahna", "lohi", "made", "muikku", "pasuri", 
                "rautu", "ruutana", "salakka", "särki", "säyne", "siika", 
                "silakka", "sorva", "suutari", "taimen", "täplärapu"
                ]
        viehet = ["uistin", "lusikka", "lippa", "jigi", "perho", "vaappu",
                  "spinnerbait", "popperi", "jerkki", "häntyri", "bladebait", 
                  "chatterbait", "spintail"
                  ]
        vavat = ["avokelavapa", "jigivapa", "haukivapa", "onki",
                "hyrräkelavapa", "umpikelavapa", "merivapa", "jäämerivapa", "perhovapa"
                ]
        for laji in lajit:
            cursor.execute(f'INSERT INTO laji (laji) VALUES ("{laji}")')
        for viehe in viehet:
            cursor.execute(f'INSERT INTO viehe (viehe) VALUES ("{viehe}")')
        for vapa in vavat:
            cursor.execute(f'INSERT INTO vapa (vapa) VALUES ("{vapa}")')
        cursor.connection.commit()       
    except ImportError:
        print("Taulukon luominen epäonnistui")
db()
