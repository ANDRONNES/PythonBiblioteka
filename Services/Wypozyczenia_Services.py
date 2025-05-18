import sqlite3
from datetime import *
from xml.etree.ElementPath import prepare_self

from Exceptions.BookNotAvailable_Exception import BookNotAvaliable_Exception
from Exceptions.RentDoesNotExists_Exception import RentDoesNotExists_Exception
from Models import Wypozyczenie
from .Ksiazki_Services import *
from .Czytelnicy_Services import *
from Exceptions import *

conn = sqlite3.connect('Data Base/biblioteka.db')
cursor = conn.cursor()


def add_new_rent():
    Id_ksiazka = int(input("Podaj id ksiazki "))
    Id_czytelnik = int(input("Podaj id czytelnika "))
    # Data_Wypozyczenia = date(input("Podaj datę wypozyczenia "))
    # Data_Zwrotu = date(input("Podaj datę zwrotu "))
    str_data_wyp = input("Podaj datę wypozyczenia (YYYY-MM-DD): ")
    str_data_zwrotu = input("Podaj datę zwrotu (YYYY-MM-DD): ")

    try:
        try:
            Data_Wypozyczenia = datetime.strptime(str_data_wyp, "%Y-%m-%d").date()
            Data_Zwrotu = datetime.strptime(str_data_zwrotu, "%Y-%m-%d").date()
        except ValueError:
            raise InvalidDateFormat_Exception
        if not isBookExists(Id_ksiazka):
            raise Invalid_KsiazkaId_Exception
        else:
            if not isReaderExists(Id_czytelnik):
                raise Invalid_CzytelnikId_Exception
            else:
                if Data_Wypozyczenia >= Data_Zwrotu:
                    raise DataConflictException
                else:
                    cursor.execute('''INSERT INTO Wypozyczenie(Ksiazka_id_ksiazki,Czytelnik_id_czytelnika,Data_Wypozyczenia,Data_Zwrotu)
                                          VALUES(?,?,?,?) ''',
                                   (Id_ksiazka, Id_czytelnik, Data_Wypozyczenia, Data_Zwrotu))
                    conn.commit()
                    print("Wypożyczenie zostało dodane do bazy")
    except Invalid_KsiazkaId_Exception:
        print("Nie ma książki o takim ID")
    except Invalid_CzytelnikId_Exception:
        print("Nie ma czytelnika o takim ID")
    except InvalidDateFormat_Exception:
        print("Nieprawidłowy format daty")
    except DataConflictException:
        print("Data wypozyczenia nie może być wcześniej niż data zwrotu")

def delete_rent():
    Id_wypozycznie = int(input("Podaj id wypozyczenia które chcesz usunąć "))
    cursor.execute('Delete from Wypozyczenie Where id_wypozyczenia = ?', (Id_wypozycznie,))
    try:
        if cursor.rowcount == 0:
            raise Invalid_WypozyczenieId_Exception
        else:
            conn.commit()
            print("wypozyczenie o id: ", Id_wypozycznie, " zostało usunięte")
    except Invalid_WypozyczenieId_Exception:
        print("Nie ma wypozyczenia o takim id")

def get_all_rents():
    cursor.execute('''SELECT w.id_wypozyczenia, k.Tytul,a.imie || ' ' || a.nazwisko AS Autor,
                      c.imie || ' ' || c.nazwisko AS Czytelnik, Data_Wypozyczenia, Data_Zwrotu
                      FROM Wypozyczenie w 
                      JOIN Ksiazka k ON w.Ksiazka_id_ksiazki = k.id_ksiazki
                      JOIN Autor a ON k.Autor_id_autora = a.id_autora
                      JOIN Czytelnik c ON w.Czytelnik_id_czytelnika = c.id_czytelnika''')

    rows = cursor.fetchall()
    rents = []
    for id_wypozyczenia, Tytul, Autor, Czytelnik, Data_Wypozyczenia, Data_Zwrotu in rows:
        rent = Wypozyczenie(id_wypozyczenia, Tytul, Autor, Czytelnik, Data_Wypozyczenia, Data_Zwrotu)
        rents.append(rent)

    if len(rows) == 0:
        # Zrobić wyjątek na puste dane?
        print("W bibliotece nie ma żadnego wypożyczenia")
    return rents

def edit_rent():
    print(get_all_rents())
    id_wypozyczenia = int(input("Podaj id wypozyczenia którą chcesz edytować "))
    try:
        cursor.execute('Select count(*) from Wypozyczenie where id_wypozyczenia = ?', (id_wypozyczenia,))
        if cursor.rowcount == 0:
            raise Invalid_WypozyczenieId_Exception
        else:
            # whatToEdit = input("Podaj który parametr wypozyczenia chcesz edytować")
            whatToEdit = int(input('''Podaj który parametr wypozyczenia chcesz edytować :
                                    Tytul - wpisz 1
                                    Czytelnik - wpisz 2
                                    Data_Wypozyczenia - wpisz 3
                                    Data_Zwrotu - wpisz 4 '''))

            match whatToEdit:
                case 1:
                    newBook_id = int(input("Podaj id ksiazki na którą chesz zamienić "))
                    try:
                        if not isBookExists(newBook_id):
                            raise Invalid_KsiazkaId_Exception
                        else:
                            cursor.execute('UPDATE Wypozyczenie SET Ksiazka_id_ksiazki = ? Where id_wypozyczenia = ?',
                                           (newBook_id, id_wypozyczenia,))
                            conn.commit()
                            print("Wypożyczona książka została zmieniona ")
                    except Invalid_KsiazkaId_Exception:
                        print("Nie ma książki o takim ID")
                case 2:
                    newCzytelnik_id = int(input("Podaj id czytelnika na którego chesz zamienić "))
                    try:
                        if not isReaderExists(newCzytelnik_id):
                            raise Invalid_CzytelnikId_Exception
                        else:
                            cursor.execute(
                                'UPDATE Wypozyczenie SET Czytelnik_id_czytelnika = ? Where id_wypozyczenia = ?',
                                (newCzytelnik_id, id_wypozyczenia,))
                            conn.commit()
                            print("Czytelnik został zmieniony")
                    except Invalid_CzytelnikId_Exception:
                        print("Nie ma czytelnika o takim ID")
                case 3:
                    newData_Wypozyczenia = date(input("Podaj datę wypozyczenia na którą chcesz zamienić "))
                    try:
                        if not datetime.strptime(newData_Wypozyczenia, '%Y-%m-%d'):
                            raise InvalidDateFormat_Exception
                        else:
                            cursor.execute('SELECT Data_Zwrotu FROM Wypozyczenia WHERE id_wypozyczenia = ?',
                                           (id_wypozyczenia,))
                            Data_Zwrotu = cursor.fetchone()[0]
                            if newData_Wypozyczenia >= Data_Zwrotu:
                                raise DataConflictException
                            else:
                                cursor.execute(
                                    'UPDATE Wypozyczenie SET Data_Wypozyczenia = ? Where id_wypozyczenia = ?',
                                    (newData_Wypozyczenia, id_wypozyczenia,))
                                conn.commit()
                                print("Data wypozyczenia została zmieniona ")
                    except InvalidDateFormat_Exception:
                        print("Nieprawidłowy format daty")
                    except DataConflictException:
                        print("Data wypozyczenia nie może być wcześniej niż data zwrotu")
                case 4:
                    newData_Zwrotu = date(input("Podaj datę zwrotu na którą chcesz zamienić "))
                    try:
                        if not datetime.strptime(newData_Zwrotu, '%Y-%m-%d'):
                            raise InvalidDateFormat_Exception
                        else:
                            cursor.execute('SELECT Data_Wypozyczenia FROM Wypozyczenia WHERE id_wypozyczenia = ?',
                                           (id_wypozyczenia,))
                            Data_Wypozyczenia = cursor.fetchone()[0]
                            if newData_Zwrotu <= Data_Wypozyczenia:
                                raise DataConflictException
                            else:
                                cursor.execute(
                                    'UPDATE Wypozyczenie SET Data_Wypozyczenia = ? Where id_wypozyczenia = ?',
                                    (newData_Zwrotu, id_wypozyczenia,))
                                conn.commit()
                                print("Data zwrotu została zmieniona ")
                    except InvalidDateFormat_Exception:
                        print("Nieprawidłowy format daty")
                    except DataConflictException:
                        print("Data zwrotu nie może być wcześniej niż data wypozyczenia")
    except Invalid_CzytelnikId_Exception:
        print("Nie ma wypozyczenia o takim ID")

def przedluzenie_wypozyczenia(id_wypozyczenia:int):
    try:
        if not isRentExists(id_wypozyczenia):
            raise RentDoesNotExists_Exception
    except RentDoesNotExists_Exception:
        print("Nie ma takiego wypożyczenia")
    try:
        dataDo = input("Podaj datę do kiedy chcesz przedłużyć wypożyczenie (yyyy-mm-dd)")
        new_Data_Zwrotu = datetime.strptime(dataDo, "%Y-%m-%d").date()
    except ValueError:
        print("podano datę w złym formacie")

    cursor.execute('SELECT Data_Zwrotu FROM Wypozyczenia WHERE id_wypozyczenia = ?',
                   (id_wypozyczenia,))
    Data_Zwrotu = cursor.fetchone()[0]

    try:
        if new_Data_Zwrotu <= Data_Zwrotu:
            raise DataConflictException

        cursor.execute('UPDATE Wypozyczenie SET Data_Zwrotu = ? WHERE id_wypozyczenia = ?  ', (new_Data_Zwrotu))
        conn.commit()
        print("Data zwrotu została zmieniona na ",Data_Zwrotu)

    except DataConflictException:
        print("Podana nowa data nie jest dalszą datą od aktualnej")

def isRentExists(id_rent:int)->bool:
    cursor.execute('Select * FROM Wypozyczenia WHERE id_wypozyczenia = ?', (id_rent,))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True