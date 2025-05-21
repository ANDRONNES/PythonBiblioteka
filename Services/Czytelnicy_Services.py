import sqlite3
from Exceptions import *
import re
from Models import Czytelnik
from Services.Adresy_Services import isAdresExists

conn = sqlite3.connect('Data Base/biblioteka.db')
cursor = conn.cursor()


def add_new_reader():
    Imie = input("Podaj imię czytelnika ")
    Nazwisko = input("Podaj nazwisko czytelnika ")
    Numer_Telefonu = input("Podaj numer telefonu czytelnika ")
    Numer_Mieszkania = int(input("Podaj numer mieszkania czytelnika "))
    Numer_Domu = int(input("Podaj numer domu czytelnika "))
    Ulica = input("Podaj ulicę czytelnika ")
    Miasto = input("Podaj miasto czytelnika ")
    pattern = r'^\+?\d+$'
    try:
        if not re.fullmatch(pattern, Numer_Telefonu):
            raise Invalid_NumerTelefonu_Exception
        else:
            if not isAdresExists(Miasto, Ulica, Numer_Domu, Numer_Mieszkania):
                raise Invalid_Adres_Exception
            else:
                cursor.execute('''Insert INTO Czytelnik(Imie,Nazwisko,Numer_Telefonu,Adres_Numer_Mieszkania,Adres_Numer_Domu,Adres_Ulica,Adres_Miasto,Naleznosc)
                              VALUES (?,?,?,?,?,?,?)''',
                               (Imie, Nazwisko, Numer_Telefonu, Numer_Mieszkania, Numer_Domu, Ulica, Miasto,0))
                conn.commit()
                print("Czytelnik został dodany do bazy")
    except Invalid_Adres_Exception:
        print("Nie istinieje takiego adresu w bazie danych")
    except Invalid_NumerTelefonu_Exception:
        print("Numer telefonu może składać się tylko z cyfr")


def delete_reader():
    idCzytelnika = int(input("podaj id czytelnika którego chcesz usunąć "))
    cursor.execute('DELETE FROM Czytelnik WHERE id_czytelnika = ?', (idCzytelnika,))

    try:
        if cursor.rowcount == 0:
            raise Invalid_CzytelnikId_Exception
        else:
            conn.commit()
            print("Czytelnik o id: ", idCzytelnika, " został usunięty")
    except Invalid_CzytelnikId_Exception:
        print("Nie istnieje czytelnika o takim id")


def get_all_readers():
    cursor.execute('SELECT * FROM Czytelnik')
    rows = cursor.fetchall()

    readers = []
    for Id_czytelnik, imie, nazwisko, numer_telefonu, numer_mieszkania, numer_domu, ulica, miasto,naleznosc in rows:
        reader = Czytelnik(Id_czytelnik, imie, nazwisko, numer_telefonu, numer_mieszkania, numer_domu, ulica, miasto,naleznosc)
        readers.append(reader)

    if len(rows) == 0:
        print("W bibliotece nie ma żadnego czytelnika")

    return readers


def edit_reader():
    print(get_all_readers())
    id_czytelnika = int(input("Podaj id czytelnika którego chcesz edytować "))
    try:
        if not isReaderExists(id_czytelnika):
            raise Invalid_CzytelnikId_Exception
        else:
            whatToEdit = int(input('''Podaj który parametr wypozyczenia chcesz edytować :
                                        Imie - wpisz 1
                                        Nazwisko - wpisz 2
                                        Numer_Telefonu - wpisz 3
                                        Adres - wpisz 4 '''))
            match whatToEdit:
                case 1:
                    newImie = input("Podaj nowe Imie ")
                    cursor.execute('UPDATE Czytelnik SET Imie = ? Where id_czytelnika = ?',
                                   (newImie, id_czytelnika,))
                    conn.commit()
                case 2:
                    newNazwisko = input("Podaj nowe Nazwisko ")
                    cursor.execute('UPDATE Czytelnik SET Nazwisko = ? Where id_czytelnika = ?',
                                   (newNazwisko, id_czytelnika,))
                    conn.commit()
                case 3:
                    newNumer_Telefonu = input("Podaj nowy Numer Telefonu ")
                    pattern = r'^\+?\d+$'
                    try:
                        if not re.fullmatch(pattern, newNumer_Telefonu):
                            raise Invalid_NumerTelefonu_Exception
                        else:
                            cursor.execute('UPDATE Czytelnik SET Numer_Telefonu = ? Where id_czytelnika = ?',
                                           (newNumer_Telefonu, id_czytelnika,))
                            conn.commit()
                    except Invalid_NumerTelefonu_Exception:
                        print("Numer telefonu może składać się tylko z cyfr")
                case 4:
                    Numer_Mieszkania = int(input("Podaj nowy numer mieszkania czytelnika "))
                    Numer_Domu = int(input("Podaj nowy numer domu czytelnika "))
                    Ulica = input("Podaj nową ulicę czytelnika ")
                    Miasto = input("Podaj nowe miasto czytelnika ")
                    try:
                        if not isAdresExists(Miasto, Ulica, Numer_Domu, Numer_Mieszkania):
                            raise Invalid_Adres_Exception
                        else:
                            cursor.execute(
                                'Update Czytelnik SET Adres_Numer_Mieszkania = ?,Adres_Numer_Domu = ?,Adres_Ulica = ?,Adres_Miasto = ?',
                                (Numer_Mieszkania, Numer_Domu, Ulica, Miasto))
                            conn.commit()
                    except Invalid_Adres_Exception:
                        print("Nie istinieje takiego adresu w bazie danych")
    except Invalid_CzytelnikId_Exception:
        print("Nie istnieje czytelnika o podanym id")

def isReaderExists(Id_czytelnik: int) -> bool:
    cursor.execute('SELECT count(*) FROM czytelnik where id_czytelnika = ?', (Id_czytelnik,))
    result = cursor.fetchone()[0]
    return result > 0

def get_all_reader_history():
    cursor.execute('''Select c.Imie || ' ' || c.Nazwisko as Czytelnik,k.Tytul,h.opis_operacji,h.data
                      from Historia h Join Czytelnik c ON h.Czytelnik_id_czytelnika = c.id_czytelnika
                      Join Ksiazka k ON k.id_ksiazki = h.Ksiazka_id_ksiazki''')
    result = cursor.fetchall()
    for row in result:
        print(row)

def get_reader_object_by_Id(Id_czytelnik: int):

    cursor.execute('SELECT * FROM Czytelnik WHERE id_czytelnika = ?', (Id_czytelnik,))
    row = cursor.fetchone()

    czytelnik = None
    if row:
        czytelnik = Czytelnik(*row)
        print(czytelnik)
    else:
        print("Czytelnik nie znaleziony.")

        return czytelnik



