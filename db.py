import sqlite3

conn = sqlite3.connect("sklep.db", check_same_thread=False)
cursor = conn.cursor()

cursor.executescript("""
    CREATE TABLE IF NOT EXISTS kategorie (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazwa TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS produkty (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nazwa TEXT NOT NULL,
        cena REAL NOT NULL,
        opis TEXT,
        ilosc INTEGER NOT NULL,
        kategoria_id INTEGER,
        FOREIGN KEY (kategoria_id) REFERENCES kategorie(id)
    );

    CREATE TABLE IF NOT EXISTS koszyk (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produkt_id INTEGER NOT NULL,
        ilosc INTEGER NOT NULL,
        sesja_id TEXT NOT NULL,
        FOREIGN KEY (produkt_id) REFERENCES produkty(id)
    );

    CREATE TABLE IF NOT EXISTS zamowienia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        data TEXT NOT NULL,
        status TEXT NOT NULL,
        suma REAL NOT NULL
    );

    CREATE TABLE IF NOT EXISTS pozycje_zamowienia (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        zamowienie_id INTEGER NOT NULL,
        produkt_id INTEGER NOT NULL,
        ilosc INTEGER NOT NULL,
        cena REAL NOT NULL,
        FOREIGN KEY (zamowienie_id) REFERENCES zamowienia(id),
        FOREIGN KEY (produkt_id) REFERENCES produkty(id)
    );
""")

conn.commit()
