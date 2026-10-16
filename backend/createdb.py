"""Create the application database schema and seed its lookup tables."""

import re

import pymysql

import dbinfo


SPECIES = (
    "ahven", "harjus", "hauki", "jokirapu", "kiiski", "kirjolohi",
    "kolmipiikki", "kuha", "kuore", "lahna", "lohi", "made", "muikku",
    "pasuri", "rautu", "ruutana", "salakka", "särki", "säyne", "siika",
    "silakka", "sorva", "suutari", "taimen", "täplärapu",
)
LURES = (
    "uistin", "lusikka", "lippa", "jigi", "perho", "vaappu",
    "spinnerbait", "popperi", "jerkki", "häntyri", "bladebait",
    "chatterbait", "spintail",
)
RODS = (
    "avokelavapa", "jigivapa", "haukivapa", "onki", "hyrräkelavapa",
    "umpikelavapa", "merivapa", "jäämerivapa", "perhovapa",
)


def create_database():
    """Create the configured database and tables, then seed lookups."""
    database_name = dbinfo.data["DBNIMI"]
    if not re.fullmatch(r"[A-Za-z0-9_]+", database_name):
        raise ValueError("Database names may contain only letters, digits, and underscores.")

    connection = pymysql.connect(
        host=dbinfo.data["HOST"],
        port=dbinfo.data["PORT"],
        user=dbinfo.data["USER"],
        password=dbinfo.data["PASSWORD"],
        charset="utf8mb4",
        autocommit=True,
    )
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{database_name}`")
        connection.select_db(database_name)
        definitions = (
            "CREATE TABLE IF NOT EXISTS admin ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "username VARCHAR(45) NOT NULL UNIQUE, "
            "pword VARCHAR(255) NOT NULL) ENGINE=InnoDB",
            "CREATE TABLE IF NOT EXISTS kalastaja ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "nimi VARCHAR(45) NOT NULL, "
            "email VARCHAR(45) NOT NULL UNIQUE, "
            "pword VARCHAR(255) NOT NULL) ENGINE=InnoDB",
            "CREATE TABLE IF NOT EXISTS viehe ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "viehe VARCHAR(64) NOT NULL UNIQUE) ENGINE=InnoDB",
            "CREATE TABLE IF NOT EXISTS vapa ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "vapa VARCHAR(64) NOT NULL UNIQUE) ENGINE=InnoDB",
            "CREATE TABLE IF NOT EXISTS laji ("
            "id INT AUTO_INCREMENT PRIMARY KEY, "
            "laji VARCHAR(64) NOT NULL UNIQUE) ENGINE=InnoDB",
            "CREATE TABLE IF NOT EXISTS tarppi ("
            "id INT AUTO_INCREMENT NOT NULL UNIQUE, "
            "aika DATETIME NOT NULL, kalastaja_id INT NOT NULL, "
            "viehe_id INT NOT NULL, vapa_id INT NOT NULL, paikka VARCHAR(64), "
            "PRIMARY KEY (id, kalastaja_id, viehe_id, vapa_id), "
            "FOREIGN KEY (kalastaja_id) REFERENCES kalastaja(id), "
            "FOREIGN KEY (viehe_id) REFERENCES viehe(id), "
            "FOREIGN KEY (vapa_id) REFERENCES vapa(id)) ENGINE=InnoDB",
            "CREATE TABLE IF NOT EXISTS kala ("
            "id INT AUTO_INCREMENT NOT NULL UNIQUE, tarppi_id INT NOT NULL, "
            "pituus FLOAT, paino FLOAT, laji_id INT NOT NULL, "
            "kuva VARCHAR(255), "
            "PRIMARY KEY (id, tarppi_id), "
            "FOREIGN KEY (tarppi_id) REFERENCES tarppi(id), "
            "FOREIGN KEY (laji_id) REFERENCES laji(id)) ENGINE=InnoDB",
        )
        with connection.cursor() as cursor:
            for statement in definitions:
                cursor.execute(statement)
            for table, column, values in (
                ("laji", "laji", SPECIES),
                ("viehe", "viehe", LURES),
                ("vapa", "vapa", RODS),
            ):
                cursor.executemany(
                    f"INSERT INTO {table} ({column}) "
                    f"SELECT %s WHERE NOT EXISTS "
                    f"(SELECT 1 FROM {table} WHERE {column} = %s)",
                    [(value, value) for value in values],
                )
    finally:
        connection.close()


if __name__ == "__main__":
    create_database()
