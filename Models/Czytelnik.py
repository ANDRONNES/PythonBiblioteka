from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Czytelnik:
    Id_czytelnik: int
    Imie: str
    Nazwisko: str
    Numer_telefonu: str
    Numer_Mieszkania: int
    Numer_Domu: int
    Ulica: str
    Miasto: str
    Naleznosc: int = 0

