from dataclasses import dataclass

@dataclass
class Ksiazka:
    # Id_ksiazki : float #int??
    Id_ksiazka : float #int??
    Tytul : str
    #Autor_id_autor : int
    Autor_id : int
    Numer_ISBN : str
    Wydawnictwo : str
    Liczba_stron : int
    #Status_id_statusu : int
    Status_id : int
