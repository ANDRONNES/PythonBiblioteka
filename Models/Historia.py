from dataclasses import dataclass

import datetime


@dataclass
class Historia:

    Id_historia : int
    IdCzytlenika : int
    IdKsiazki : int
    Opis_operacji:str
    data : datetime
