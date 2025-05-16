import sqlite3

conn = sqlite3.connect('biblioteka.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE Wypozyczenie (
    id_wypozyczenia integer NOT NULL CONSTRAINT Wypozyczenie_pk PRIMARY KEY,
    Ksiazka_id_ksiazki double precision NOT NULL,
    Czytelnik_id_czytelnika integer NOT NULL,
    Data_Wypozyczenia date NOT NULL,
    Data_Zwrotu date NOT NULL,
    CONSTRAINT Wypozyczenie_Ksiazka FOREIGN KEY (Ksiazka_id_ksiazki)
    REFERENCES Ksiazka (id_ksiazki)
    ON DELETE CASCADE,
    CONSTRAINT Wypozyczenie_Czytelnik FOREIGN KEY (Czytelnik_id_czytelnika)
    REFERENCES Czytelnik (id_czytelnika)
    ON DELETE CASCADE
);
''')