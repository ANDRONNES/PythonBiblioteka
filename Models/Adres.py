from dataclasses import dataclass


@dataclass
class Adres:
    Miasto: str
    Ulica: str
    Numer_Domu: int
    Numer_Mieszkania: int
