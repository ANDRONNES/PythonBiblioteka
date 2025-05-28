import sqlite3
from datetime import *
import pandas as pd
from tabulate import tabulate
from Exceptions import *
from Models import Rezerwacja
from Services import *

conn = sqlite3.connect('Data Base/biblioteka.db')
cursor = conn.cursor()

def validated_input(prompt, cast_func=int, error_msg="Niepoprawna wartość. Spróbuj ponownie."):
    while True:
        user_input = input(prompt)
        try:
            return cast_func(user_input)
        except Exception:
            print(error_msg)

def input_non_empty(prompt="Wprowadź wartość: "):
    while True:
        user_input = input(prompt).strip()
        if user_input:
            return user_input
        else:
            print("Wartość nie może być pusta. Spróbuj ponownie.")


def add_new_reservation():
    print(tabulate(get_all_books(), headers='keys', tablefmt='fancy_grid'))
    try:
        Id_ksiazka = validated_input("Podaj id ksiazki ")
        if not isBookExists(Id_ksiazka):
            raise Invalid_KsiazkaId_Exception
        elif not isBookAvailable(Id_ksiazka):
            raise BookNotAvaliable_Exception
        else:
            print(tabulate(get_all_readers(), headers='keys', tablefmt='fancy_grid'))
            Id_czytelnik = validated_input("Podaj id czytelnika ")
            if not isReaderExists(Id_czytelnik):
                raise Invalid_RezerwacjaId_Exception
            else:
                try:
                    str_data_rozp = input_non_empty("Podaj datę rozpoczęcia rezerwacji (YYYY-MM-DD): ")
                    Data_rozpoczecnia_rezerwacji = datetime.strptime(str_data_rozp, "%Y-%m-%d").date()
                except ValueError:
                    raise InvalidDateFormat_Exception

                try:
                    str_data_zak = input_non_empty("Podaj datę zakończenia rezerwacji (YYYY-MM-DD): ")
                    Data_zakonczenia_rezerwacji = datetime.strptime(str_data_zak, "%Y-%m-%d").date()
                except ValueError:
                    raise InvalidDateFormat_Exception

                if Data_rozpoczecnia_rezerwacji >= Data_zakonczenia_rezerwacji:
                    raise DataConflictException()
                else:
                    cursor.execute('''
                    INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                    VALUES (?,?,?,?)''',(Id_czytelnik, Id_ksiazka, "Rezerwacja", Data_zakonczenia_rezerwacji))

                    cursor.execute('''
                    INSERT INTO Rezerwacja (Ksiazka_id_ksiazki,Czytelnik_id_czytelnika,Data_rozpoczecia,Data_zakonczenia) 
                    VALUES(?,?,?,?)''', (Id_ksiazka, Id_czytelnik, Data_rozpoczecnia_rezerwacji, Data_zakonczenia_rezerwacji))
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


def isReservationExists(id_rezerwacji: int) -> bool:
    cursor.execute('Select count(*) from Rezerwacja WHERE id_rezerwacji = ?', (id_rezerwacji,))
    result = cursor.fetchone()[0]
    return result > 0


def delete_reservation():
    print(tabulate(get_all_reservations(), headers='keys', tablefmt='fancy_grid'))
    try:
        Id_rezerwacji = validated_input("Podaj id rezerwacji którą chcesz usunąć ")
        if not isReservationExists(Id_rezerwacji):
            raise Invalid_RezerwacjaId_Exception
        else:
            cursor.execute('SELECT Ksiazka_id_ksiazki FROM Rezerwacja WHERE id_rezerwacji = ?', (Id_rezerwacji,))
            idKsiazki = cursor.fetchone()[0]

            cursor.execute('Delete from Rezerwacja Where id_rezerwacji = ?', (Id_rezerwacji,))
            cursor.execute('UPDATE Ksiazka SET Status_id_statusu = 1 WHERE id_ksiazki = ? ', (idKsiazki,))
            conn.commit()
            print("Rezerwacja o id: ", Id_rezerwacji, " zostało usunięte")
    except Invalid_RezerwacjaId_Exception:
        print("Nie ma rezerwacji o takim id")


def get_all_reservations():
    cursor.execute('''
    SELECT Id_rezerwacji, Ksiazka.id_ksiazki,Ksiazka.Tytul,Czytelnik.id_czytelnika,Czytelnik.Imie,Rezerwacja.Data_rozpoczecia,Rezerwacja.Data_zakonczenia
    FROM Rezerwacja
    JOIN Ksiazka ON Rezerwacja.Ksiazka_id_ksiazki = Ksiazka.id_ksiazki
    JOIN Czytelnik ON Czytelnik.id_czytelnika = Rezerwacja.Czytelnik_id_czytelnika
    ''')

    rows = cursor.fetchall()
    reservations = []
    for Id_rezerwacji, id_ksiazki, Tytul, id_czytelnika, Imie, Data_rozpoczecia, Data_zakonczenia in rows:
        reserv = Rezerwacja(Id_rezerwacji, id_ksiazki, Tytul, id_czytelnika, Imie, Data_rozpoczecia, Data_zakonczenia)
        reservations.append(reserv)

    if len(rows) == 0:
        raise NoReservationException("W bibliotece nie ma żadnych rezerwacji")

    df = pd.DataFrame(reservations)
    return df


def edit_reservation():
    print(tabulate(get_all_reservations(), headers='keys', tablefmt='fancy_grid'))
    id_rezerwacji = validated_input("Podaj id rezerwacji którą chcesz edytować ")
    try:
        if not isReservationExists(id_rezerwacji):
            raise Invalid_RezerwacjaId_Exception
        else:
            whatToEdit = validated_input('''Wybierz akcję którą chcesz wykonać: 
1. Zmień książkę
2. Zmień czytelnika
3. Zmień Datę rospoczęcia rezerwacji
4. Zmień Datę zakończenia rezerwacji
5. Wyjdź\n''')

            match whatToEdit:
                case 1:
                    print(tabulate(get_all_books(), headers='keys', tablefmt='fancy_grid'))
                    newBook_id = validated_input("Podaj id ksiazki na którą chesz zamienić ")
                    try:
                        if not isBookExists(newBook_id):
                            raise Invalid_KsiazkaId_Exception
                        else:
                            cursor.execute('SELECT Ksiazka_id_ksiazki FROM Rezerwacja Where id_rezerwacji = ? ',(id_rezerwacji,))
                            oldBook = cursor.fetchone()[0]

                            cursor.execute('Update Ksiazka set Status_id_statusu = 1 where id_ksiazki = ?', (oldBook,))

                            cursor.execute('Select Czytelnik_id_czytelnika from Rezerwacja Where id_rezerwacji = ?',(id_rezerwacji,))
                            czytelnik = cursor.fetchone()[0]

                            cursor.execute('''
                            Insert INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                            Values(?,?,?,?)''',(czytelnik, newBook_id, "Wymiana rezerwowanej książki", date.today()))

                            cursor.execute('Select Status_id_statusu From Ksiazka Where id_ksiazki = ?', (newBook_id,))
                            if cursor.fetchone()[0] == 1:
                                cursor.execute('UPDATE Rezerwacja SET Ksiazka_id_ksiazki = ? Where id_rezerwacji = ?',(newBook_id, id_rezerwacji,))

                                cursor.execute('Update Ksiazka set Status_id_statusu = 3 where id_ksiazki = ?',(newBook_id,))

                                cursor.execute('UPDATE Rezerwacja SET Ksiazka_id_ksiazki = ? Where id_rezerwacji = ?',(newBook_id, id_rezerwacji,))
                                conn.commit()
                                print("Rezerwowana książka została zmieniona ")
                            else:
                                raise BookNotAvaliable_Exception
                    except Invalid_KsiazkaId_Exception:
                        print("Nie ma książki o takim ID")
                    except BookNotAvaliable_Exception:
                        print("Książka nie jest dostępna")
                case 2:
                    print(tabulate(get_all_readers(), headers='keys', tablefmt='fancy_grid'))
                    try:
                        newCzytelnik_id = validated_input("Podaj id czytelnika na którego chesz zamienić ")
                        cursor.execute('Select Czytelnik_id_czytelnika From rezerwacja where id_rezerwacji = ?',(id_rezerwacji,))

                        if (newCzytelnik_id == cursor.fetchone()[0]):
                            raise DataConflictException
                        else:
                            if not isReaderExists(newCzytelnik_id):
                                raise Invalid_CzytelnikId_Exception
                            else:
                                cursor.execute(
                                    'UPDATE Rezerwacja SET Czytelnik_id_czytelnika = ? Where id_rezerwacji = ?',(newCzytelnik_id, id_rezerwacji,))

                                cursor.execute('Select Ksiazka_id_ksiazki from rezerwacja Where id_wypozyczenia = ?',(id_rezerwacji,))
                                bookId = cursor.fetchone()[0]

                                cursor.execute('''
                                Insert INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                                Values(?,?,?,?)''',(newCzytelnik_id, bookId,"Rezerwacja (zmiana czytelnika w rezerwacji)", date.today()))

                                conn.commit()
                                print("Czytelnik został zmieniony")
                    except Invalid_CzytelnikId_Exception:
                        print("Nie ma czytelnika o takim ID")
                    except DataConflictException:
                        print("Nie można zmienić czytelnika na tego samego")

                case 3:
                    newData_Rezerwacji = input_non_empty("Podaj datę rezerwacji na którą chcesz zamienić ")
                    try:
                        Data_Rezerwacji = datetime.strptime(newData_Rezerwacji, "%Y-%m-%d").date()
                        cursor.execute('SELECT Data_zakonczenia FROM Rezerwacja WHERE id_rezerwacji = ?',(id_rezerwacji,))
                        Data_Zwrotu = datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d").date()
                        if Data_Rezerwacji >= Data_Zwrotu:
                            raise DataConflictException
                        else:
                            cursor.execute(
                                'Select Czytelnik_id_czytelnika,Ksiazka_id_ksiazki from Rezerwacja WHERE id_rezerwacji = ?',(id_rezerwacji,))
                            values = cursor.fetchone()

                            cursor.execute('''
                            INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                            VALUES (?,?,?,?)''',(values[0], values[1], "Przeniesienie rozpoczęcia rezerwacji",date.today()))

                            cursor.execute('UPDATE Rezerwacja SET Data_rozpoczecia = ? Where id_rezerwacji = ?',(newData_Rezerwacji, id_rezerwacji,))
                            conn.commit()
                            print("Data rezerwacji została zmieniona ")
                    except ValueError:
                        raise InvalidDateFormat_Exception
                    except InvalidDateFormat_Exception:
                        print("Nieprawidłowy format daty")
                    except DataConflictException:
                        print("Data rozpoczecia nie może być wcześniejsza niż data zakonczenia")
                case 4:
                    newData_Zwrotu = input_non_empty("Podaj datę zakonczenia rezerwacji na którą chcesz zamienić ")
                    try:
                        Data_Zwrotu = datetime.strptime(newData_Zwrotu, "%Y-%m-%d").date()
                        cursor.execute('SELECT Data_zakonczenia FROM Rezerwacja WHERE id_rezerwacji = ?',(id_rezerwacji,))

                        Data_Wypozyczenia = datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d").date()
                        if Data_Zwrotu <= Data_Wypozyczenia:
                            raise DataConflictException
                        else:
                            cursor.execute(
                                'Select Czytelnik_id_czytelnika,Ksiazka_id_ksiazki from Rezerwacja WHERE id_rezerwacji = ?',(id_rezerwacji,))
                            values = cursor.fetchone()
                            cursor.execute('''
                            INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                            VALUES (?,?,?,?)''',(values[0], values[1], "Przeniesienie zakończenia rezerwacji",date.today()))

                            cursor.execute('UPDATE Rezerwacja SET Data_rozpoczecia = ? Where id_rezerwacji = ?',(newData_Zwrotu, id_rezerwacji,))
                            conn.commit()
                            print("Data zakonczenia rezerwacji została zmieniona ")
                    except ValueError:
                        raise InvalidDateFormat_Exception
                    except InvalidDateFormat_Exception:
                        print("Nieprawidłowy format daty")
                    except DataConflictException:
                        print("Data zakoczenia nie może być wcześniej niż data rozpoczecia")
                case 5:
                    return -1
    except Invalid_RezerwacjaId_Exception:
        print("Nie ma rezerwacji o takim ID")
