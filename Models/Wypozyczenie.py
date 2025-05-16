from dataclasses import dataclass
from datetime import date


@dataclass
class Wypozyczenie:
    # Id_wypozyczenia: int
    Id_wypozyczenie: int
    # Ksiazka_id_ksiazki : float
    Id_ksiazka: float
    # Czytelnik_id_czetelnika : int
    Id_Czytelnik: int
    Data_Wypozyczenie: date  # datetime?
    Data_Zwrotu: date  # datetime?
