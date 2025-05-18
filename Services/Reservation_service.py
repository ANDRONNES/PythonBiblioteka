import sqlite3
from datetime import *
import pandas as pd

from Exceptions import InvalidDateFormat_Exception, Invalid_KsiazkaId_Exception, DataConflictException, \
    Invalid_CzytelnikId_Exception
from Exceptions.BookNotAvailable_Exception import BookNotAvaliable_Exception
from Exceptions.Invalid_RezerwacjaId_Exception import Invalid_RezerwacjaId_Exception
from Exceptions.No_Reservation_Exception import NoReservationException
from Models import Rezerwacja
from Services.Czytelnicy_Services import isReaderExists, cursor
from Services.Ksiazki_Services import isBookExists, isBookAvailable, isBookReserved

conn = sqlite3.connect('Data Base/biblioteka.db')
cursor = conn.cursor()

def add_new_reservation():
    Id_ksiazka = int(input("Podaj id ksiazki "))
    Id_czytelnik = int(input("Podaj id czytelnika "))
    str_data_rozp = input("Podaj datę rozpoczęcia rezerwacji (YYYY-MM-DD): ")
    str_data_zak = input("Podaj datę zakończenia rezerwacji (YYYY-MM-DD): ")

    try:
        try:
            Data_rozpoczecnia_rezerwacji = datetime.strptime(str_data_rozp, "%Y-%m-%d").date()
            Data_zakonczenia_rezerwacji = datetime.strptime(str_data_zak, "%Y-%m-%d").date()
        except ValueError:
            raise InvalidDateFormat_Exception()

        if not isBookExists(Id_ksiazka):
            raise Invalid_KsiazkaId_Exception()
        else:
            if not isReaderExists(Id_czytelnik):
                raise Invalid_CzytelnikId_Exception()
            else:
                if Data_rozpoczecnia_rezerwacji >= Data_zakonczenia_rezerwacji:
                    raise DataConflictException()
                else:
                    if not isBookAvailable(Id_ksiazka):
                        raise BookNotAvaliable_Exception()
                    else:
                        cursor.execute('''INSERT INTO Rezerwacja (Ksiazka_id_ksiazki,Czytelnik_id_czytelnika,Data_rozpoczecia,Data_zakonczenia) 
                        VALUES(?,?,?,?)''', (Id_ksiazka, Id_czytelnik,Data_rozpoczecnia_rezerwacji, Data_zakonczenia_rezerwacji))
                        conn.commit()
                        cursor.execute('UPDATE Ksiazka SET Status_id_statusu = 3 WHERE id_ksiazki = ? ', (Id_ksiazka,))
                        conn.commit()
                        print("Rezerwacja została dodana")

    except Invalid_KsiazkaId_Exception:
        print("Nie ma książki o takim ID")
    except Invalid_CzytelnikId_Exception:
        print("Nie ma czytelnika o takim ID")
    except InvalidDateFormat_Exception:
        print("Nieprawidłowy format daty")
    except BookNotAvaliable_Exception:
        print("Książka nie jest teraz dostępna w bibliotece")
    except DataConflictException:
        print("Data wypozyczenia nie może być wcześniej niż data zwrotu")

def delete_reservation():
    Id_rezerwacji = int(input("Podaj id wypozyczenia które chcesz usunąć "))
    cursor.execute('SELECT Ksiazka_id_ksiazki FROM Rezerwacja WHERE id_rezerwacji = ?', (Id_rezerwacji,) )
    idKsiazki = cursor.fetchone()[0]

    cursor.execute('Delete from Rezerwacja Where id_rezerwacji = ?', (Id_rezerwacji,))
    try:
        if cursor.rowcount == 0:
            raise Invalid_RezerwacjaId_Exception
        else:
            conn.commit()
            print("Rezerwacja o id: ", Id_rezerwacji, " zostało usunięte")
    except Invalid_RezerwacjaId_Exception:
        print("Nie ma rezerwacji o takim id")

    cursor.execute('UPDATE Ksiazka SET Status_id_statusu = 1 WHERE id_ksiazki = ? ', (idKsiazki,))
    conn.commit()


def get_all_reservations():
    cursor.execute('''SELECT Id_rezerwacji, Ksiazka.id_ksiazki,Ksiazka.Tytul,Czytelnik.id_czytelnika,Czytelnik.Imie,Rezerwacja.Data_rozpoczecia,Rezerwacja.Data_zakonczenia
    FROM Rezerwacja
    JOIN Ksiazka ON Rezerwacja.Ksiazka_id_ksiazki = Ksiazka.id_ksiazki
    JOIN Czytelnik ON Czytelnik.id_czytelnika = Rezerwacja.Czytelnik_id_czytelnika''')

    rows = cursor.fetchall()
    reservations = []
    for Id_rezerwacji, id_ksiazki, Tytul, id_czytelnika,Imie, Data_rozpoczecia, Data_zakonczenia in rows:
        reserv = Rezerwacja(Id_rezerwacji, id_ksiazki, Tytul, id_czytelnika ,Imie, Data_rozpoczecia, Data_zakonczenia)
        reservations.append(reserv)

    if len(rows) == 0:
     raise NoReservationException("W bibliotece nie ma żadnych rezerwacji")

    df = pd.DataFrame(reservations)
    return df

def edit_reservation():
    print(get_all_reservations())
    id_rezerwacji = int(input("Podaj id rezerwacji którą chcesz edytować "))
    try:
        cursor.execute('Select count(*) from Rezerwacja where id_rezerwacji = ?', (id_rezerwacji,))
        if cursor.rowcount == 0:
            raise Invalid_RezerwacjaId_Exception
        else:
            # whatToEdit = input("Podaj który parametr wypozyczenia chcesz edytować")
            whatToEdit = int(input('''Podaj który parametr wypozyczenia chcesz edytować :
                                    Książka - wpisz 1
                                    Czytelnik - wpisz 2
                                    Data rozpoczecia rezerwacji - wpisz 3
                                    Data zakończenia rezerwacji - wpisz 4 '''))

            match whatToEdit:
                case 1:
                    newBook_id = int(input("Podaj id ksiazki na którą chesz zamienić "))
                    try:
                        if not isBookExists(newBook_id):
                            raise Invalid_KsiazkaId_Exception
                        else:
                            cursor.execute('UPDATE Rezerwacja SET Ksiazka_id_ksiazki = ? Where id_rezerwacji = ?',
                                           (newBook_id, id_rezerwacji,))
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
                                'UPDATE Rezerwacja SET Czytelnik_id_czytelnika = ? Where id_rezerwacji = ?',
                                (newCzytelnik_id, id_rezerwacji,))
                            conn.commit()
                            print("Czytelnik został zmieniony")
                    except Invalid_CzytelnikId_Exception:
                        print("Nie ma czytelnika o takim ID")
                case 3:
                    newData_Wypozyczenia = date(input("Podaj datę rezerwacji na którą chcesz zamienić "))
                    try:
                        if not datetime.strptime(newData_Wypozyczenia, '%Y-%m-%d'):
                            raise InvalidDateFormat_Exception
                        else:
                            cursor.execute('SELECT Data_zakonczenia FROM Rezerwacja WHERE id_rezerwacji = ?',
                                           (id_rezerwacji,))
                            Data_Zwrotu = cursor.fetchone()[0]
                            if newData_Wypozyczenia >= Data_Zwrotu:
                                raise DataConflictException
                            else:
                                cursor.execute(
                                    'UPDATE Rezerwacja SET Data_rozpoczecia = ? Where id_rezerwacji = ?',
                                    (newData_Wypozyczenia, id_rezerwacji,))
                                conn.commit()
                                print("Data rezerwacji została zmieniona ")
                    except InvalidDateFormat_Exception:
                        print("Nieprawidłowy format daty")
                    except DataConflictException:
                        print("Data rozpoczecia nie może być wcześniejsza niż data zakonczenia")
                case 4:
                    newData_Zwrotu = date(input("Podaj datę zakonczenia rezerwacji na którą chcesz zamienić "))
                    try:
                        if not datetime.strptime(newData_Zwrotu, '%Y-%m-%d'):
                            raise InvalidDateFormat_Exception
                        else:
                            cursor.execute('SELECT Data_zakonczenia FROM Rezerwacja WHERE id_rezerwacji = ?',
                                           (id_rezerwacji,))
                            Data_Wypozyczenia = cursor.fetchone()[0]
                            if newData_Zwrotu <= Data_Wypozyczenia:
                                raise DataConflictException
                            else:
                                cursor.execute(
                                    'UPDATE Rezerwacja SET Data_rozpoczecia = ? Where id_rezerwacji = ?',
                                    (newData_Zwrotu, id_rezerwacji,))
                                conn.commit()
                                print("Data zakonczenia rezerwacji została zmieniona ")
                    except InvalidDateFormat_Exception:
                        print("Nieprawidłowy format daty")
                    except DataConflictException:
                        print("Data zakoczenia nie może być wcześniej niż data rozpoczecia")
    except Invalid_CzytelnikId_Exception:
        print("Nie ma rezerwacji o takim ID")


