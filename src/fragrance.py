import os
from enum import Enum

# TODO decide if I'm going to use this or not, seems kinda useless
class Conc(Enum):
    PARFUM = ("Parfum", "Pure Parfum", "Extrait", "Extrait de Parfum")
    EDP = ("Eau De Parfum", "EDP")
    EDT = ("EDT", "Eau De Toilette")
    COLOGNE = ("EDC", "Cologne", "Eau De Cologne")

class Fragrance():
    def __init__(self, brand: str, name: str, my_score: int | None = None):
        # required
        self.brand = brand
        self.name = name
        # optional
        self.my_score = my_score
        # modified
        # self.concentration = None
        # self.public_score = None
        # self.accords = None
        # self.notes = None
        # self.card = os.path.abspath(f'./db/cards/{self.brand}/{self.name}')
        # self.link = f'https://www.fragrantica.com/designers/{self.brand}.html'

    def __repr__(self) -> str:
        name = f'{self.brand} - {self.name}'
        name_score = f'{self.brand} - {self.name} ({self.my_score})'
        if self.my_score == None:
            return name
        else:
            return name_score
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            if self.brand == other.brand and self.name == other.name:
                return True
        return False

    