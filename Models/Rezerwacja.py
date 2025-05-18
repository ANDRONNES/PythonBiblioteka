
from dataclasses import dataclass
from datetime import date


@dataclass
class Rezerwacja:
    Id_rezerwacji: int
    Id_ksiazki: int
    Tytul_ksiazja:str
    Id_czytelnika: int
    Imie_czytelnika: str
    Data_rozpoczecia : date
    Data_zakonczenia : date


