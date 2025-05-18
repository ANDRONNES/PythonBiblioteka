
from Services.Czytelnicy_Services import add_new_reader, get_all_readers
from Services.Ksiazki_Services import add_new_book, get_all_books, delete_book, edit_book

from tabulate import tabulate

from Services.Reservation_service import add_new_reservation, get_all_reservations
from Services.Wypozyczenia_Services import add_new_rent, get_all_rents, delete_rent

from Services.Czytelnicy_Services import add_new_reader, get_all_readers, edit_reader
from Services.Ksiazki_Services import add_new_book, get_all_books, delete_book
from Services.Wypozyczenia_Services import add_new_rent, get_all_rents, delete_rent, edit_rent, return_book


# add_new_book()
booksList = get_all_books()
print(tabulate(booksList, headers='keys', tablefmt='fancy_grid'))

# delete_book()
#edit_book()

# add_new_reader()
# readers = get_all_readers()
# print(readers)

# add_new_rent()
# rents = get_all_rents()
# print(rents)
# delete_rent()


#add_new_reservation()
print(tabulate(get_all_reservations(), headers='keys', tablefmt='fancy_grid'))


# add_new_rent()
# edit_rent()
rents = get_all_rents()
print(rents)
# delete_rent()

# edit_reader()

# add_new_rent()
# add_new_book()
# add_new_rent()
# return_book()
