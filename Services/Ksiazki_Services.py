


import sqlite3

from Models import Ksiazka

conn = sqlite3.connect('Data Base/biblioteka.db')
cursor = conn.cursor()

def add_new_book():
    tytul = input("Podaj tutuł książki ")
    autor_imie = input("Podaj imie autora ")
    autor_nazwisko = input("Podaj nazwisko autora ")
    isbn = input("Podaj numer isbn ")
    wydawnictwo = input("Podaj wydawnictwo ")
    l_stron = input("Podaj liczbe stron ")
    l_stron = int(l_stron)
    status = input("Podaj status ")


    while(True):
        id_status = get_status_id(status)
        if id_status == -1:
            status = input("Nie znaleziono takiego statusu, podaj status ponownie, dostepne statusy to: Dostępna / Wypożyczona / Zarezerwowana ")
        else:
            break




    id_autora= None
    cursor.execute('SELECT id_autora FROM Autor WHERE imie = ? AND Nazwisko = ?', (autor_imie,autor_nazwisko))
    row = cursor.fetchone()

    if row is None:
        cursor.execute('INSERT INTO Autor (Imie,Nazwisko) VALUES (?,?)', (autor_imie,autor_nazwisko))
        cursor.execute('SELECT id_autora FROM Autor WHERE imie = ? AND Nazwisko = ?', (autor_imie,autor_nazwisko))
        row = cursor.fetchone()

    id_autora = row[0]

    cursor.execute('''
                INSERT INTO Ksiazka (Tytul, Autor_id_autora, Numer_ISBN, Wydawnictwo, Liczba_stron, Status_id_statusu)
                VALUES (?, ?, ?, ?, ?, ?)
                ''', (tytul, id_autora, isbn, wydawnictwo, l_stron, id_status))

    conn.commit()
    print("Książka została dodana do bazy")

def get_status_id(nazwa_statusu:str):
    cursor.execute('SELECT * FROM Status WHERE Nazwa = ? ', (nazwa_statusu,))
    row = cursor.fetchone()
    if row is None:
        return -1
    else:
        return row[0]

def delete_book():
    idKsiazki = int(input("podaj id ksiązki którą chcesz usunąć"))
    cursor.execute('DELETE FROM Ksiazka WHERE id_ksiazki = ?', (idKsiazki,))

    if cursor.rowcount == 0:
        print("Nie ma książki o takim id")
    conn.commit()

    print("książka o id: ",idKsiazki, "została usunięta")

def get_all_books():
    cursor.execute('SELECT id_ksiazki, Tytul,Autor.Imie,Autor.Nazwisko,Numer_ISBN,Wydawnictwo,Status.Nazwa,Liczba_stron FROM Ksiazka JOIN Status on Ksiazka.Status_id_statusu = Status.id_statusu JOIN Autor ON Ksiazka.Autor_id_autora = Autor.id_autora' )
    rows  = cursor.fetchall()

    books = []
    for id_ksiazki, tytul,autor_imie,autor_nazwisko, numer_isbn,wydawnictwo, liczba_Stron,status, in rows:
     book = Ksiazka(id_ksiazki,tytul,autor_imie,autor_nazwisko,numer_isbn,wydawnictwo,liczba_Stron,status)
     books.append(book)


    if len(rows) == 0:
        print("W bibliotece nie ma żadnej książki")

    return books

def edit_book():
    id_ksiazki = input("Podaj id ksiazki którą chesz edytować ")
    whatToEdit = input("Podaj który parametr książki chesz edytować ")
    match whatToEdit:
        case "Tytul":
            title =input("Podaj nowy tytuł ")
            cursor.execute('UPDATE Ksiazka SET Tytul = ? WHERE id_ksiazki =?',(title,id_ksiazki))
            conn.commit()
            print("Tytuł książki został zmieniony ")
        case "Numer_ISBN":
            isbn = input("Podaj nowy ISBN ")
            cursor.execute('UPDATE Ksiazka SET Numer_ISBN = ? WHERE id_ksiazki =?', (isbn, id_ksiazki))
            conn.commit()
            print("ISBN książki został zmieniony ")
        case "Wydawnictwo":
            wydawnictwo = input("Podaj nowe wydawnictwo ")
            cursor.execute('UPDATE Ksiazka SET Wydawnictwo = ? WHERE id_ksiazki =?', (wydawnictwo, id_ksiazki))
            conn.commit()
            print("Wydawnictwo książki zostało zmienione ")
        case "Liczba_stron":
            liczba_stron = input("Podaj nową lcizbe stron ")
            cursor.execute('UPDATE Ksiazka SET Liczba_stron = ? WHERE id_ksiazki =?', (liczba_stron, id_ksiazki))
            conn.commit()
            print("Liczba stron książki została zmieniona")
        case "Statu":
            status = input("Podaj nowy status")

            while (True):
                id_status = get_status_id(status)
                if id_status == -1:
                    status = input(
                        "Nie znaleziono takiego statusu, podaj status ponownie, dostepne statusy to: Dostępna / Wypożyczona / Zarezerwowana ")
                else:
                    break

            cursor.execute('UPDATE Ksiazka SET Status_id_statusu = ? WHERE id_ksiazki =?', (id_status, id_ksiazki))
            conn.commit()
            print("Status ksiązki został zmieniony")


def isBookExists(id_ksiazki : int) -> bool:
    cursor.execute('Select count(*) from Ksiazka where id_ksiazki = ? ',(id_ksiazki,))
    result = cursor.fetchone()[0]
    return result > 0

