```mermaid
---
title:  Kalastus ER-kaavio
config:
    layout: elk
---
erDiagram
    direction RL
    KALASTAJA ||--o{ TARPPI: saa
    VIEHE ||--o{ TARPPI: liittyy
    VAPA ||--o{ TARPPI: liittyy
    KALA }o--|| TARPPI: saa
    LAJI ||--o{ KALA: liittyy

    TARPPI {
        int id PK
        datetime aika
        int kalastaja_id
        int viehe_id
        int vapa_id
        string paikka
    }

    KALASTAJA {
        int id PK
        string nimi
        string email
        string password

    } 

    VIEHE {
        int id PK
        string viehe
    }    
    
    KALA {
        int id PK
        int tarppi_id
        float pituus
        float paino
        int laji_id
    }

    VAPA {
        int id PK
        string vapa
    }
    
    LAJI {
        int id PK
        string laji
    }