from dataclasses import dataclass


@dataclass
class Czytelnik:
    # Id_czytelnika: int
    Id_czytelnik: int
    Imie: str
    Nazwisko: str
    Numer_telefonu: float  # str?
    # Adres_Numer_Mieszkania : int
    Numer_Mieszkania: int
    # Adres_Numer_Domu : int
    Numer_Domu: int
    # Adres_Ulica : str
    Ulica: str
    # Adres_Miasto : str
    Miasto: str
