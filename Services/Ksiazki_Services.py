import sqlite3
import pandas as pd
from colorama import Fore, Style
from tabulate import tabulate
from Exceptions import *
from Models import Ksiazka

conn = sqlite3.connect('Data Base/biblioteka.db')
cursor = conn.cursor()

def validated_input(prompt, cast_func=int, error_msg="Niepoprawna wartość. Spróbuj ponownie."):
    while True:
        user_input = input(prompt)
        try:
            return cast_func(user_input)
        except Exception:
            print(error_msg)


def get_status_id(nazwa_statusu: str):
    cursor.execute('SELECT * FROM Status WHERE Nazwa = ? ', (nazwa_statusu,))
    row = cursor.fetchone()
    if row is None:
        return -1
    else:
        return row[0]


def delete_book():
    print(tabulate(get_all_books(), headers='keys', tablefmt='fancy_grid'))
    idKsiazki = validated_input("podaj id ksiązki którą chcesz usunąć ")
    cursor.execute('DELETE FROM Ksiazka WHERE id_ksiazki = ?', (idKsiazki,))

    if cursor.rowcount == 0:
        print("Nie ma książki o takim id")
    conn.commit()

    print("książka o id: ", idKsiazki, "została usunięta")


def koloruj_status(status):
    if status == "Dostępna":
        return f"{Fore.GREEN}{status}{Style.RESET_ALL}"
    elif status == "Wypożyczona":
        return f"{Fore.RED}{status}{Style.RESET_ALL}"
    elif status == "Zarezerwowana":
        return f"{Fore.YELLOW}{status}{Style.RESET_ALL}"
    else:
        return status


def get_all_books():
    cursor.execute('''
        SELECT id_ksiazki, Tytul, Autor.Imie, Autor.Nazwisko,Numer_ISBN, Wydawnictwo, Status.Nazwa, Liczba_stron
        FROM Ksiazka
        JOIN Status ON Ksiazka.Status_id_statusu = Status.id_statusu
        JOIN Autor ON Ksiazka.Autor_id_autora = Autor.id_autora
    ''')
    rows = cursor.fetchall()

    if len(rows) == 0:
        raise No_Books_Exception("W bibliotece nie ma aktualnie żadnych książek")

    books = []
    for id_ksiazki, tytul, autor_imie, autor_nazwisko, numer_isbn, wydawnictwo, status, liczba_stron in rows:
        books.append({
            "Id książki": str(id_ksiazki),
            "Tytuł": tytul,
            "Imie autora": autor_imie,
            "Nazwisko autora": autor_nazwisko,
            "ISBN": numer_isbn,
            "Wydawnictwo": wydawnictwo,
            "Status": status,
            "Liczba stron": str(liczba_stron)
        })

    df = pd.DataFrame(books)
    df["Status"] = df["Status"].apply(koloruj_status)
    return df

    return books


def edit_book():
    print(tabulate(get_all_books(), headers='keys', tablefmt='fancy_grid'))
    try:
        id_ksiazki = input("Podaj id ksiazki którą chesz edytować ")
        if not isBookExists(id_ksiazki):
            raise Invalid_KsiazkaId_Exception
        else:
            whatToEdit = validated_input('''Wybierz parametr który chcesz edytować: 
1. Tytul
2. Numer_ISBN 
3. Wydawnictwo
4. Liczba_stron
5. Status
6. Wyjdź\n''')

            try:
                match whatToEdit:
                    case 1:
                        title = input("Podaj nowy tytuł ")
                        cursor.execute('UPDATE Ksiazka SET Tytul = ? WHERE id_ksiazki =?', (title, id_ksiazki))
                        conn.commit()
                        print("Tytuł książki został zmieniony ")
                    case 2:
                        isbn = input("Podaj nowy ISBN ")
                        cursor.execute('UPDATE Ksiazka SET Numer_ISBN = ? WHERE id_ksiazki =?', (isbn, id_ksiazki))
                        conn.commit()
                        print("ISBN książki został zmieniony ")
                    case 3:
                        wydawnictwo = input("Podaj nowe wydawnictwo ")
                        cursor.execute('UPDATE Ksiazka SET Wydawnictwo = ? WHERE id_ksiazki =?',
                                       (wydawnictwo, id_ksiazki))
                        conn.commit()
                        print("Wydawnictwo książki zostało zmienione ")
                    case 4:
                        liczba_stron = input("Podaj nową lcizbe stron ")
                        cursor.execute('UPDATE Ksiazka SET Liczba_stron = ? WHERE id_ksiazki =?',
                                       (liczba_stron, id_ksiazki))
                        conn.commit()
                        print("Liczba stron książki została zmieniona")
                    case 5:
                        status = input("Podaj nowy status ")

                        while (True):
                            id_status = get_status_id(status)
                            if id_status == -1:
                                status = input(
                                    "Nie znaleziono takiego statusu, podaj status ponownie, dostepne statusy to: Dostępna / Wypożyczona / Zarezerwowana ")
                            else:
                                break

                        cursor.execute('UPDATE Ksiazka SET Status_id_statusu = ? WHERE id_ksiazki =?',(id_status, id_ksiazki))
                        conn.commit()
                        print("Status ksiązki został zmieniony")
                    case 6:
                        return -1
                    case _:
                        print("Nie rozpoznano operacji, spróbuj ponownie")
            except Unknown_Operation_Exception:
                print("Nie rozpoznano operacji")
    except Invalid_KsiazkaId_Exception:
        print("Nie ma książki o takim id")


def isBookExists(id_ksiazki: int) -> bool:
    cursor.execute('Select count(*) from Ksiazka where id_ksiazki = ? ', (id_ksiazki,))
    result = cursor.fetchone()[0]
    return result > 0


def isBookAvailable(id_ksiazki: int) -> bool:
    cursor.execute('Select * from Ksiazka where id_ksiazki = ? AND Status_id_statusu = ? ', (id_ksiazki, 1))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True


def isBookReserved(id_ksiazki: int) -> bool:
    cursor.execute('Select * FROM Ksiazka WHERE id_ksiazki = ? AND Status_id_statusu = 3 ', (id_ksiazki,))
    row = cursor.fetchone()
    if row is None:
        return False
    else:
        return True


def add_new_book_prompt():
    tytul = input("Podaj tutuł książki: ")
    autor_imie = input("Podaj imie autora: ")
    autor_nazwisko = input("Podaj nazwisko autora: ")
    isbn = input("Podaj numer ISBN: ")
    wydawnictwo = input("Podaj wydawnictwo: ")
    l_stron = validated_input("Podaj liczbe stron: ")
    status = input("Podaj status: ")

    add_new_book(tytul, autor_imie, autor_nazwisko, isbn, wydawnictwo, l_stron, status)


def addDuplicateBook():
    allBooks = get_all_books()
    # print(allBooks)
    print(tabulate(allBooks, headers='keys', tablefmt='fancy_grid'))
    id_ksiazki = input("Podaj id książki, którą chcesz duplikować: ")
    try:
        if not isBookExists(id_ksiazki):
            raise Invalid_KsiazkaId_Exception
        else:
            cursor.execute('''
                SELECT k.Tytul, a.Imie, a.Nazwisko, k.Numer_ISBN, k.Wydawnictwo, k.Liczba_stron, s.Nazwa
                FROM Ksiazka k
                JOIN Autor a ON k.Autor_id_autora = a.id_autora
                JOIN Status s ON k.Status_id_statusu = s.id_statusu
                WHERE k.id_ksiazki = ?
            ''', (id_ksiazki,))
            row = cursor.fetchone()

            if row:
                tytul, autor_imie, autor_nazwisko, isbn, wydawnictwo, l_stron, status = row
                add_new_book(tytul, autor_imie, autor_nazwisko, isbn, wydawnictwo, l_stron, 'Dostępna')
                print("Dodano kopię książki:", tytul)
            else:
                print("Nie znaleziono książki o podanym ID.")

    except Invalid_KsiazkaId_Exception:
        print("Nie znaleziono książki o podanym ID.")


def add_new_book(tytul, autor_imie, autor_nazwisko, isbn, wydawnictwo, l_stron, status):
    while (True):
        id_status = get_status_id(status)
        if id_status == -1:
            status = input(
                "Nie znaleziono takiego statusu, podaj status ponownie, dostepne statusy to: Dostępna / Wypożyczona / Zarezerwowana ")
        else:
            break

    id_autora = None
    cursor.execute('SELECT id_autora FROM Autor WHERE imie = ? AND Nazwisko = ?', (autor_imie, autor_nazwisko))
    row = cursor.fetchone()

    if row is None:
        cursor.execute('INSERT INTO Autor (Imie,Nazwisko) VALUES (?,?)', (autor_imie, autor_nazwisko))
        cursor.execute('SELECT id_autora FROM Autor WHERE imie = ? AND Nazwisko = ?', (autor_imie, autor_nazwisko))
        row = cursor.fetchone()

    id_autora = row[0]

    cursor.execute('''
                INSERT INTO Ksiazka (Tytul, Autor_id_autora, Numer_ISBN, Wydawnictwo, Liczba_stron, Status_id_statusu)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (tytul, id_autora, isbn, wydawnictwo, l_stron, id_status))

    conn.commit()
    print("Książka została dodana do bazy")
