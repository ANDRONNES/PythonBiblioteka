from Services.Czytelnicy_Services import add_new_reader, get_all_readers
from Services.Ksiazki_Services import add_new_book, get_all_books, delete_book
from Services.Wypozyczenia_Services import add_new_rent, get_all_rents, delete_rent

#add_new_book()
booksList = get_all_books()
print(booksList)
#delete_book()

# add_new_reader()
readers = get_all_readers()
print(readers)

add_new_rent()
rents = get_all_rents()
print(rents)
# delete_rent()