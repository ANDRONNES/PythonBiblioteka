from unittest import case
import colorama
from colorama import Fore, Style
from tabulate import tabulate
from Services import *


# Wojtek, jeszcze zostały metody:
# Czetelnicy:
# get_all_reader_history(CztelnikId : int)
# get_reader_object_by_Id



print("Witaj w systemie bibliotecznym")

while(True):
    decision = int(input('''Wybierz akcję którą chcesz wykonać: 
1. Akcje związane z czytelnikiem
2. Akcje związane z książką
3. Wypożyczenia 
4. Rezerwacje 
5. Wyjdź\n'''))

    match decision:
        case 1:
            czytlenik_decision = int(input('''
1. Dodaj czytelnika
2. Usuń czytelnika
3. Edytuj dane czytelnika
4. Wyświetl dane wszystkich czytelników
5. Wyświetl historię danego czytelnika
6. Wróć\n'''))
            match czytlenik_decision:
                case 1:
                    add_new_reader()
                case 2:
                    delete_reader()
                case 3:
                    edit_reader()
                case 4:
                    print(tabulate(get_all_readers(), headers='keys', tablefmt='fancy_grid'))
                case 5:
                    headers = ["Imię", "Nazwisko", "Tytuł Książki","Operacja","Data Operacji"]
                    print(tabulate(get_all_reader_history(), headers=headers, tablefmt='fancy_grid'))
                case 6:
                    continue
                case _:
                    print(Fore.RED +"\nWybrano niepoprawną operację!git a\n"+ Style.RESET_ALL)
                    continue

        case 2:
            ksiazka_decision = int(input('''Wybierz akcję którą chcesz wykonać: 
1. Dodaj książkę
2. Usuń książkę
3. Edytuj dane książki
4. Wyświetl dane wszytskich książek
5. Wróć\n'''))
            match ksiazka_decision:
                case 1:
                    nowa_czy_duplikat= int(input('''Chcesz dodać:
1. Nową książkę
2. Duplikat
3. Wróć\n'''))
                    match nowa_czy_duplikat:
                        case 1:
                            add_new_book_prompt()
                        case 2:
                            addDuplicateBook()
                        case 3:
                            continue
                        case _:
                            print(Fore.RED +"\nWybrano niepoprawną operację!\n"+ Style.RESET_ALL)
                            continue

                case 2:
                    delete_book()
                case 3:
                    edit_book()
                case 4:
                    print(tabulate(get_all_books(), headers='keys', tablefmt='fancy_grid'))
                case 5:
                    continue
                case _:
                    print(Fore.RED +"\nWybrano niepoprawną operację!\n"+ Style.RESET_ALL)
                    continue

        case 3:
            wypozyczenie_decision = int(input('''Wybierz akcję którą chcesz wykonać:"
1. Utwórz wypozyczenie
2. Usuń wypozyczenie
3. Edytuj wypozyczenie
4. Zwróć książkę
5. Wyświetl wszystkie wypożyczenia
6. Przedłuż wypożyczenie
7. Wróć\n'''))
            match wypozyczenie_decision:
                case 1:
                    add_new_rent()
                case 2:
                    delete_rent()
                case 3:
                    edit_rent()
                case 4:
                    return_book()
                case 5:
                    print(tabulate(get_all_rents(), headers='keys', tablefmt='fancy_grid'))
                case 6:
                    przedluzenie_wypozyczenia()
                case 7:
                    continue
                case _:
                    print(Fore.RED +"\nWybrano niepoprawną operację!\n"+ Style.RESET_ALL)
                    continue

        case 4:
            rezerwacja_decision = int(input('''Wybierz akcję którą chcesz wykonać:
1. Utwórz rezerwację
2. Usuń rezerwację
3. Edytuj rezerwację
4. Wyświetl wszystkie rezerwacje
5. Wróć\n'''))
            match rezerwacja_decision:
                case 1:
                    add_new_reservation()
                case 2:
                    delete_reservation()
                case 3:
                    edit_reservation()
                case 4:
                    print(tabulate(get_all_reservations(), headers='keys', tablefmt='fancy_grid'))
                case 5:
                    continue
                case _:
                    print(Fore.RED + "\nWybrano niepoprawną operację!\n"+ Style.RESET_ALL)
                    continue
        case 5:
            break
        case _:
            print(Fore.RED +"\nNie rozpoznano operacji!\n"+ Style.RESET_ALL)
            continue

# add_new_book()
# booksList = get_all_books()
# print(tabulate(booksList, headers='keys', tablefmt='fancy_grid'))

# delete_book()
# edit_book()

#add_new_reader()
# readers = get_all_readers()

# print(tabulate(readers, headers='keys', tablefmt='fancy_grid'))

# add_new_rent()
# rents = get_all_rents()
# print(tabulate(rents, headers='keys', tablefmt='fancy_grid'))
# delete_rent()


#add_new_reservation()
# print(tabulate(get_all_reservations(), headers='keys', tablefmt='fancy_grid'))


# add_new_rent()
# edit_rent()
# rents = get_all_rents()
# print(rents)
# delete_rent()

# edit_reader()

# add_new_rent()
# for i in range(5):
#     addDuplicateBook()
# add_new_book_prompt()
# add_new_rent()
# return_book()





# add_new_reader()
# add_new_reservation()
# edit_reservation()
# add_new_rent()
# przedluzenie_wypozyczenia(3)  #need to add print
# get_all_reader_history() #need to add imie nazwisko instead of id or a completely different outcome