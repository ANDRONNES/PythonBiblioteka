from dataclasses import dataclass


@dataclass
class Rezerwacja:
    Id_rezerwacja: int
    Id_ksiazka: int
    Id_Czytelnik: int
