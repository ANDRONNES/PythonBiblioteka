import sqlite3
from tabulate import tabulate
from Exceptions import *
import re
from Models import Czytelnik, Historia

conn = sqlite3.connect('Data Base/biblioteka.db')
cursor = conn.cursor()

def validated_input(prompt, cast_func=int, error_msg="Niepoprawna wartość. Spróbuj ponownie."):
    while True:
        user_input = input(prompt)
        try:
            return cast_func(user_input)
        except Exception:
            print(error_msg)

def add_new_reader():
    Imie = input("Podaj imię czytelnika ")
    Nazwisko = input("Podaj nazwisko czytelnika ")
    Numer_Telefonu = input("Podaj numer telefonu czytelnika ")
    Numer_Mieszkania = validated_input("Podaj numer mieszkania czytelnika ")
    Numer_Domu = validated_input("Podaj numer domu czytelnika ")
    Ulica = input("Podaj ulicę czytelnika ")
    Miasto = input("Podaj miasto czytelnika ")
    pattern = r'^\+?\d+$'
    try:
        if not re.fullmatch(pattern, Numer_Telefonu):
            raise Invalid_NumerTelefonu_Exception
        else:
            cursor.execute('''Insert INTO Czytelnik(Imie,Nazwisko,Numer_Telefonu,Adres_Numer_Mieszkania,Adres_Numer_Domu,Adres_Ulica,Adres_Miasto,Naleznosc)
                            VALUES (?,?,?,?,?,?,?,?)''',
                           (Imie, Nazwisko, Numer_Telefonu, Numer_Mieszkania, Numer_Domu, Ulica, Miasto, 0))
            conn.commit()
            print("Czytelnik został dodany do bazy")
    except Invalid_NumerTelefonu_Exception:
        print("Numer telefonu może składać się tylko z cyfr")


def delete_reader():
    print(tabulate(get_all_readers(), headers='keys', tablefmt='fancy_grid'))
    idCzytelnika = validated_input("podaj id czytelnika którego chcesz usunąć ")
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
    for Id_czytelnik, imie, nazwisko, numer_telefonu, numer_mieszkania, numer_domu, ulica, miasto, naleznosc in rows:
        reader = Czytelnik(Id_czytelnik, imie, nazwisko, numer_telefonu, numer_mieszkania, numer_domu, ulica, miasto,naleznosc)
        readers.append(reader)

    if len(rows) == 0:
        print("W bibliotece nie ma żadnego czytelnika")

    return readers


def edit_reader():
    print(tabulate(get_all_readers(), headers='keys', tablefmt='fancy_grid'))
    id_czytelnika = validated_input("Podaj id czytelnika którego chcesz edytować ")
    try:
        if not isReaderExists(id_czytelnika):
            raise Invalid_CzytelnikId_Exception
        else:
            whatToEdit = validated_input('''Wybierz parametr który chcesz edytować: 
1. Imie
2. Nazwisko 
3. Numer_Telefonu
4. Adres\n''')
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
                    Numer_Mieszkania = validated_input("Podaj nowy numer mieszkania czytelnika ")
                    Numer_Domu = validated_input("Podaj nowy numer domu czytelnika ")
                    Ulica = input("Podaj nową ulicę czytelnika ")
                    Miasto = input("Podaj nowe miasto czytelnika ")

                    cursor.execute(
                        'Update Czytelnik SET Adres_Numer_Mieszkania = ?,Adres_Numer_Domu = ?,Adres_Ulica = ?,Adres_Miasto = ? where id_czytelnika = ?',
                        (Numer_Mieszkania, Numer_Domu, Ulica, Miasto, id_czytelnika,))
                    conn.commit()

    except Invalid_CzytelnikId_Exception:
        print("Nie istnieje czytelnika o podanym id")


def isReaderExists(Id_czytelnik: int) -> bool:
    cursor.execute('SELECT count(*) FROM czytelnik where id_czytelnika = ?', (Id_czytelnik,))
    result = cursor.fetchone()[0]
    return result > 0


def get_all_reader_history():
    print(tabulate(get_all_readers(), headers='keys', tablefmt='fancy_grid'))
    Id_czytelnik = validated_input("Podaj id czytelnika którego historię chcesz wyświetlić ")
    # exception? jeśli podac literę to wypierdoli cały program

    hisotryList = []
    try:
        if not isReaderExists(Id_czytelnik):
            raise Invalid_CzytelnikId_Exception
        else:
            cursor.execute('''Select Imie, Nazwisko as Czytelnik,k.Tytul,h.opis_operacji,h.data
                              from Historia h Join Czytelnik c ON h.Czytelnik_id_czytelnika = c.id_czytelnika
                              Join Ksiazka k ON k.id_ksiazki = h.Ksiazka_id_ksiazki
                              Where c.id_czytelnika = ?''', (Id_czytelnik,))
            result = cursor.fetchall()
            for id_historia, Id_czytelnika, IdKsiazki, Opis_operacji, data in result:
                hisotria = Historia(id_historia, Id_czytelnika, IdKsiazki, Opis_operacji, data)
                hisotryList.append(hisotria)

            if len(result) == 0:
                print("Brak historii czytelnika")
            else:
                return hisotryList
    except Invalid_CzytelnikId_Exception:
        print("Nie istnieje czytelnika o podanym id")


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
