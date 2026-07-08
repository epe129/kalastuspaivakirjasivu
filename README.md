# Kalastuspäiväkirja- sivu

- currently developing new backend

Versio: 0.2 


Tämä on nettisivu, jossa on tkinter backend, johon admin voi kirjautua ja poistaa käyttäjiä, lajeja, vieheitä ja vapoja. php frondend jossa käyttäjä voi kirjautua/rekisteröityä jonka jälkeen hän voi lisätä tietoja tietokantaan ja nähdä eri tietoja kalasaaleista esim. eri kalalajien saanti määrät.

# Teknologiat: 
- Frondend: PHP
- Backned: Python tkinter
- Tietokanta: SQL database

# Tarvitaan:
- XAMPP
- Python
- phpmyadmin database

# Venv luominen
Mene terminaalissa backend kansioon:
```
cd backend 
```
Luo venv ja aktivoi venv:
```
python -m venv venv
venv\Scripts\activate
```
Huom: venv pitää olla aktivoituna kun asenna paketit

Lataa tarvittavat paketit:
```
pip install -r requirements.txt
```

# Tietokannan luonti

## Backend:
Luo dbinfo.py backend nimiseen kansioon ja laita sinne databasen yhdistämiseen tarvittavat tiedot:
```
data = {
  "USER":'esimnerkki',
  "PASSWORD":'esimnerkki',
  "DBNIMI": 'esimnerkki',
  "PORT": 1234,
  "HOST": '123.1.2.3',
} 
```
Aja databasen luonti:
```
python createdb.py
```
## Frondend:
Luo config.php data nimiseen kansioon ja laita sinne databasen yhdistämiseen tarvittavat tiedot:
```
return array(
    "serverinnimi" => "esimnerkki",
    "kayttajannimi" => "esimnerkki",
    "salasana" => "esimnerkki",
    "dbnimi" => "esimnerkki",
);
```

# Ohjelman suorittaminen
Tkinter ohjelma:
```
python backend.py
```

# Sivu
Huom: url saattaa olla hieman eri kun kloonat repositoryn.

PHP sivu:
```
http://localhost/kalastustietosivu/frondend/
```

# License
Open source.
