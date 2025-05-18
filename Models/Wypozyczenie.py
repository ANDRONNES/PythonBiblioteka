from dataclasses import dataclass
from datetime import date


@dataclass
class Wypozyczenie:
    Id_wypozyczenie: int
    Tytul : str
    Status : str
    Autor : str
    Czytelnik : str
    Data_Wypozyczenia: date
    Data_Zwrotu: date


