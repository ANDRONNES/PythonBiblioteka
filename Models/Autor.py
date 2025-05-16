from dataclasses import dataclass


@dataclass
class Autor:
    # Id_autora: int
    Id_autor: int
    Imie: str
    Nazwisko: str


"""
@dataclass pozwala na napisanie bardziej krótkiego kodu
zamiast takiego:
"""
# class Autor:
#     def __init__(self, Id_autora: int, Imie: str, Nazwisko: str):
#         self.Id_autora = Id_autora
#         self.Imie = Imie
#         self.Nazwisko = Nazwisko
