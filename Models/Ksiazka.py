from dataclasses import dataclass

@dataclass
class Ksiazka:

    Id_ksiazka : int
    Tytul : str
    Autor_imie : str
    Autor_nazwisko:str
    Numer_ISBN : str
    Wydawnictwo : str
    status_ksiazki: int
    Liczba_stron : int