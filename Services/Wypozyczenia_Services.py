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
    str_data_wyp = input("Podaj datę wypozyczenia (YYYY-MM-DD): ")
    str_data_zwrotu = input("Podaj datę zwrotu (YYYY-MM-DD): ")

    # zmienic status ksiazki

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
                    cursor.execute('Select Status_id_statusu FROM Ksiazka Where id_ksiazki = ?', (Id_ksiazka,))
                    if cursor.fetchone()[0] != 1:
                        raise Ksiazka_NieJestDostepna_Exception
                    else:
                        cursor.execute('''INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                                          VALUES (?,?,?,?)''',
                                       (Id_czytelnik, Id_ksiazka,"Wypożyczenie", Data_Wypozyczenia))

                        cursor.execute('''INSERT INTO Wypozyczenie(Ksiazka_id_ksiazki,Czytelnik_id_czytelnika,Data_Wypozyczenia,Data_Zwrotu)
                                          VALUES(?,?,?,?) ''',
                                       (Id_ksiazka, Id_czytelnik, Data_Wypozyczenia, Data_Zwrotu))
                        cursor.execute('''UPDATE Ksiazka SET Status_id_statusu = 2 Where id_ksiazki = ?''',
                                       (Id_ksiazka,))
                    conn.commit()
                    print("Wypożyczenie zostało dodane do bazy")
    except Ksiazka_NieJestDostepna_Exception:
        print("Książka nie jest teraz dostępna")
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
    cursor.execute('''SELECT w.id_wypozyczenia, k.Tytul,s.Nazwa,a.imie || ' ' || a.nazwisko AS Autor,
                      c.imie || ' ' || c.nazwisko AS Czytelnik, Data_Wypozyczenia, Data_Zwrotu
                      FROM Wypozyczenie w 
                      JOIN Ksiazka k ON w.Ksiazka_id_ksiazki = k.id_ksiazki
                      JOIN Autor a ON k.Autor_id_autora = a.id_autora
                      JOIN Czytelnik c ON w.Czytelnik_id_czytelnika = c.id_czytelnika
                      JOIN Status s ON k.Status_id_statusu = s.id_statusu''')

    rows = cursor.fetchall()
    rents = []
    for id_wypozyczenia, Tytul, Status, Autor, Czytelnik, Data_Wypozyczenia, Data_Zwrotu in rows:
        rent = Wypozyczenie(id_wypozyczenia, Tytul, Status, Autor, Czytelnik, Data_Wypozyczenia, Data_Zwrotu)
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
                    newData_Wypozyczenia = input("Podaj datę wypozyczenia na którą chcesz zamienić ")
                    try:
                        Data_Wypozyczenia = datetime.strptime(newData_Wypozyczenia, "%Y-%m-%d").date()

                        cursor.execute('SELECT Data_Zwrotu FROM Wypozyczenie WHERE id_wypozyczenia = ?',
                                       (id_wypozyczenia,))
                        Data_Zwrotu = datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d").date()
                        if Data_Wypozyczenia >= Data_Zwrotu:
                            raise DataConflictException
                        else:
                            cursor.execute(
                                'Select Czytelnik_id_czytelnika,Ksiazka_id_ksiazki from Wypozyczenie WHERE id_wypozyczenia = ?',
                                (id_wypozyczenia,))
                            values = cursor.fetchone()
                            cursor.execute('''INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                                                                                                      VALUES (?,?,?,?)''',
                                           (values[0], values[1],
                                            "Przeniesienie rozpoczęcia wypozyczenia",date.today()))
                            cursor.execute(
                                'UPDATE Wypozyczenie SET Data_Wypozyczenia = ? Where id_wypozyczenia = ?',
                                (Data_Wypozyczenia, id_wypozyczenia,))
                            conn.commit()
                            print("Data wypozyczenia została zmieniona ")
                    except ValueError:
                        raise InvalidDateFormat_Exception
                    except InvalidDateFormat_Exception:
                        print("Nieprawidłowy format daty")
                    except DataConflictException:
                        print("Data wypozyczenia nie może być wcześniej niż data zwrotu")
                case 4:
                    newData_Zwrotu = input("Podaj datę zwrotu na którą chcesz zamienić ")
                    try:
                        Data_Zwrotu = datetime.strptime(newData_Zwrotu, "%Y-%m-%d").date()
                        cursor.execute('SELECT Data_Wypozyczenia FROM Wypozyczenie WHERE id_wypozyczenia = ?',
                                       (id_wypozyczenia,))
                        Data_Wypozyczenia = datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d").date()
                        if Data_Zwrotu <= Data_Wypozyczenia:
                            raise DataConflictException
                        else:
                            cursor.execute(
                                'Select Czytelnik_id_czytelnika,Ksiazka_id_ksiazki from Wypozyczenie WHERE id_wypozyczenia = ?',
                                (id_wypozyczenia,))
                            values = cursor.fetchone()
                            cursor.execute('''INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                                                  VALUES (?,?,?,?)''',(values[0], values[1], "Przeniesienie zakończenia wypozyczenia",date.today()))



                            #jak i rezerwacja, czy nie jest to przedłużenie???




                            cursor.execute(
                                'UPDATE Wypozyczenie SET Data_Wypozyczenia = ? Where id_wypozyczenia = ?',
                                (Data_Zwrotu, id_wypozyczenia,))
                            conn.commit()
                            print("Data zwrotu została zmieniona ")
                    except ValueError:
                        raise InvalidDateFormat_Exception
                    except DataConflictException:
                        print("Data zwrotu nie może być wcześniej niż data wypozyczenia")
    except Invalid_CzytelnikId_Exception:
        print("Nie ma wypozyczenia o takim ID")
    except InvalidDateFormat_Exception:
        print("Nieprawidłowy format daty")


def przedluzenie_wypozyczenia():
    id_wypozyczenia = int(input("Podaj id wypożyczenia które chcesz przedłużyć"))
    try:
        if not isRentExists(id_wypozyczenia):
            raise RentDoesNotExists_Exception
    except RentDoesNotExists_Exception:
        print("Nie ma takiego wypożyczenia")
    try:
        dataDo = input("Podaj datę do kiedy chcesz przedłużyć wypożyczenie (yyyy-mm-dd) ")
        new_Data_Zwrotu = datetime.strptime(dataDo, "%Y-%m-%d").date()
    except ValueError:
        print("podano datę w złym formacie")

    cursor.execute('SELECT Data_Zwrotu FROM Wypozyczenie WHERE id_wypozyczenia = ?',
                   (id_wypozyczenia,))
    Data_Zwrotu = datetime.strptime(cursor.fetchone()[0], "%Y-%m-%d").date()

    try:
        if new_Data_Zwrotu <= Data_Zwrotu:
            raise DataConflictException

        cursor.execute(
            'Select Czytelnik_id_czytelnika,Ksiazka_id_ksiazki from Wypozyczenie WHERE id_wypozyczenia = ?',
            (id_wypozyczenia,))
        values = cursor.fetchone()
        cursor.execute('''INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                                                                                                              VALUES (?,?,?,?)''',
                       (values[0], values[1],  "Przedłużenie wypozyczenia",date.today()))

        cursor.execute('UPDATE Wypozyczenie SET Data_Zwrotu = ? WHERE id_wypozyczenia = ?  ', (new_Data_Zwrotu, id_wypozyczenia))
        conn.commit()
        print("Data zwrotu została zmieniona na ", new_Data_Zwrotu)

    except DataConflictException:
        print("Podana nowa data nie jest dalszą datą od aktualnej")


def isRentExists(id_rent: int) -> bool:
    cursor.execute('Select * FROM Wypozyczenie WHERE id_wypozyczenia = ?', (id_rent,))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True


def return_book():
    id_czytelnika = int(input("Podaj id czytelnika, który chce zwrócić książkę "))
    try:
        if not isReaderExists(id_czytelnika):
            raise Invalid_CzytelnikId_Exception
        else:
            cursor.execute('SELECT count(*) FROM Wypozyczenie WHERE Czytelnik_id_czytelnika = ?', (id_czytelnika,))
            if cursor.fetchone()[0] > 1:
                cursor.execute("Select * from Wypozyczenie Where Czytelnik_id_czytelnika = ?", (id_czytelnika,))
                wypozyczenia = cursor.fetchall()
                for row in wypozyczenia:
                    print(
                        f"ID wypożyczenia: {row[0]}, ID książki: {row[1]}, ID czytelnika: {row[2]}, Data wypożyczenia: {row[3]}, Data zwrotu: {row[4]}")
                id_ksiazka = input("Podaj ID książki, którą chcesz zwrócić. ")
                bool_found = False
                for row in wypozyczenia:
                    if str(row[1]) == str(id_ksiazka):
                        bool_found = True
                        break
                if not bool_found:
                    raise Invalid_KsiazkaId_Exception
                else:

                    cursor.execute('''INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                                           VALUES (?,?,?,?)''',(id_czytelnika, id_ksiazka, "Zwrot książki",date.today()))

                    cursor.execute('Update Ksiazka set Status_id_statusu = 1 Where id_ksiazki = ?', (id_ksiazka,))
                    cursor.execute(
                        'Update Wypozyczenie set Data_Zwrotu = ? Where Czytelnik_id_czytelnika = ? And Ksiazka_id_ksiazki = ?',
                        (date.today(), id_czytelnika, id_ksiazka))
                    conn.commit()
                    print("Ksiazka o Id: ", id_ksiazka, " została zwrócona ")


                    # pobieram statrą datę zwrotu do obliczenia długu
                    cursor.execute('SELECT Data_Zwrotu FROM Wypozyczenia WHERE Czytelnik_id_czytelnika = ? AND Ksiazka_id_ksiazki = ?',
                                   (id_czytelnika,id_ksiazka))
                    old_data_zwrotu = cursor.fetchone()
                    if old_data_zwrotu < date.today():
                        roznica = date.today() - old_data_zwrotu
                        roznica_days = roznica.days
                        dlug = roznica_days * 0, 50
                        print("Użytkownik o id ", id_czytelnika, " musi uregulować należność w wysokości ", dlug, " zł")
                        cursor.execute('UPDATE Czytlenik SET Naleznosc = ? WHERE id_czytelnika = ? ',
                                       (dlug * 100, id_czytelnika))

            else:

                cursor.execute('''Select id_ksiazki From Ksiazka k 
                                  JOIN Wypozyczenie w On k.id_ksiazki = w.Ksiazka_id_ksiazki
                                  JOIN Czytelnik c ON c.id_czytelnika = w.Czytelnik_id_czytelnika
                                  Where w.Czytelnik_id_czytelnika = ?''',(id_czytelnika,))
                id_ksiazki = cursor.fetchone()

                #pobieram statrą datę zwrotu do obliczenia długu
                cursor.execute('SELECT Data_Zwrotu FROM Wypozyczenia WHERE Czytelnik_id_czytelnika = ?',
                               (id_czytelnika,))
                old_data_zwrotu = cursor.fetchone()



                cursor.execute('''INSERT INTO Historia(Czytelnik_id_czytelnika,Ksiazka_id_ksiazki,opis_operacji,data)
                                                           VALUES (?,?,?,?)''',
                               (id_czytelnika, id_ksiazki[0], "Zwrot książki", date.today()))

                cursor.execute('''Update Ksiazka set Status_id_statusu = 1 
                                       Where id_ksiazki = (Select Ksiazka_id_ksiazki 
                                       From Wypozyczenie Where id_czytelnika = ?)''', (id_czytelnika,))
                cursor.execute(
                    'Update Wypozyczenie set Data_Zwrotu = ? Where Czytelnik_id_czytelnika = ?',
                    (date.today(), id_czytelnika))
                conn.commit()
                print("Ksiazka została zwrócona ")

                if old_data_zwrotu < date.today():
                    roznica = date.today() - old_data_zwrotu
                    roznica_days = roznica.days
                    dlug = roznica_days * 0,50
                    print("Użytkownik o id ",id_czytelnika, " musi uregulować należność w wysokości ",dlug, " zł")
                    cursor.execute('UPDATE Czytlenik SET Naleznosc = ? WHERE id_czytelnika = ? ',(dlug*100,id_czytelnika))


    except Invalid_CzytelnikId_Exception:
        print("Nie ma czytelnika o takim ID")
    except Invalid_KsiazkaId_Exception:
        print("Podaj prawidłowy ID książki")
