# Kalastuspäiväkirja sivusto – raportti

Versio: 0.2

## Johdanto

Tämän projektin tavoitteena oli toteuttaa kalasaaliiden tallennukseen tarkoitettu nettisivu, jossa käyttäjät voivat lisätä ja tarkastella kalastustietoja. Projektin avulla harjoittelin ohjelmointia, tietokantoja ja web-kehitystä.

---

# Projektin tavoite

Projektin tavoitteena oli tehdä toimiva nettisivu kalasaaliiden tallentamiseen ja hallintaan. Nettisivun avulla käyttäjät voivat:

* rekisteröityä
* kirjautua sisään
* lisätä kalasaaliita
* tarkastella omia tallennettuja kalatietoja

Sekä toimiva backend johon admin voi kirjautua ja poistaa:

* käyttäjiä
* lajeja
* vapoja
* vieheitä

---

# Käytetyt teknologiat

Projektissa käytettiin seuraavia teknologioita:

* Frontend: PHP 
* Database: MySQL 
* Backend: Python 
* Tkinter: Python-pohjaisen käyttöliittymän tekemiseen
* XAMPP: paikallisen palvelinympäristön käyttämiseen

---

# Tietokanta

Tietokanta suunniteltiin kalasaaliiden tallennukseen. Tietokannassa on omat taulut:

* tarpeille
* käyttäjille
* kaloille
* kalalajeille
* vieheille
* vavoille

Tietokannan relaatiot mahdollistavat tietojen yhdistämisen ja hakemisen tehokkaasti.

## Tietokantarakenne

* KALASTAJA → käyttäjätiedot
* TARPPI → yksi saatu kala / tapahtuma
* KALA → kalan tiedot
* LAJI → kala lajit
* VIEHE → vieheet
* VAPA → vavat

![Kuva tietokannasta](database.png)

---

# Ohjelman rakenne

## Frontend

Frontend toteutettiin PHP:llä. Frontendissä käyttäjä voi:

* rekisteröityä
* kirjautua
* lisätä saaliita
* tarkastella tietoja

Frondnend rakenne:

data kansio:

* data/db_connetion.php: Luodaan yhteys tietokantaan
* data/handleAdd.php: Käsittelee uuden kalasaaliin lisäämisen
* data/handleLogin.php: Käsittelee sisään kirjautumisen
* data/handleLogout.php: Käsittelee ulos kirjautumisen
* data/handleMuuAdd.php: Käsittelee uuden vapa, laji ja viehe arvon lisäämisen
* data/handleRegister.php: Käsittelee rekisteröitymisen

login kansio:

* login/login.php: Kirjautumis-sivu

main kansio:

* main/index.php: Näytetään kalasaaliiden eri tiedot
* main/lisaa.php: Uusien kalalajien lisäämissivu

Frondend:

* /index.php: Rekisteröitymis-sivu

## Backend

Backend toteutettiin Pythonilla ja Tkinterillä. Backendin tarkoituksena on ylläpitää tietokannan sisältöä.

Backendissä admin voi kirjautua sisään jonka jälkeen hän voi:

* poistaa käyttäjiä
* poistaa vieheitä
* poistaa vapoja
* poistaa kalalajeja

Backend rakenne:

* backend/backend.py: Luodaan adminin kirjautumisikkuna
* backend/admin_window.py: Luodaan admin ikkuna jossa admin voi poistaa eri tietoja
* backend/poista_moduuli.py: Moduuli tiedosto eri tietojen poisto functioille
* backend/tarkista_moduuli.py: Moduuli tiedosto functiolle joka päivittää input hakua
* backend/createdb.py: Tiedosto databasen luontiin

---

# Tietoturva

Projektissa huomioitiin perustason tietoturva:

* käyttäjien salasanat tallennetaan password_hash()-hashattuina
* SQL-injektioita estetään prepared statementien avulla

---

# Mikä onnistui

Frontend onnistui hyvin. Käyttöliittymästä tuli toimiva ja käyttäjä pystyy lisäämään sekä tarkastelemaan kalasaaliita helposti.
Tietokannan rakenne onnistui myös hyvin ja eri taulujen väliset suhteet toimivat suunnitellusti.

---

# Kehitys ideoita tulevaisuudelle

Kun jatkan projektia tulevaisuudessa, toteutan backendin Flaskilla Tkinterin sijaan. Flask sopii paremmin web-pohjaiseen sovellukseen ja helpottaa backendin laajentamista tulevaisuudessa. Parantaa tietoturvaa frondendissä.
Lisätä että käyttäjä voi poistaa omia kalasaaliita. Lisätä erikseen sivu jossa käyttäjä näkee kaikki saaliit. Rajoittaa että ei nää kun vaikka ekat 5 saalista etusivulla.

---

# Mitä opin

Projektin aikana opin lisää:

* PHP-ohjelmoinnista
* Python-ohjelmoinnista
* Tietokantojen käytöstä ja tekemisestä

Opin myös käyttämään prepared statementteja sekä salasanojen turvallista hashäystä.

---

# Yhteenveto

Projektissa toteutettiin toimiva kalasaaliiden tallennusnettisivu käyttäen PHP:tä, Pythonia ja MySQL-tietokantaa. Projekti kehitti osaamistani erityisesti web-kehityksessä, tietokannoissa ja ohjelmistojen rakenteen suunnittelussa.
