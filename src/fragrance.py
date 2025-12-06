import os


class Fragrance():
    def __init__(self, brand: str, name: str, my_score: int | None = None):
        # required
        self.brand = brand
        self.name = name
        # optional
        self.my_score = my_score
        # generated
        self.fragrantica = {
            "designer": self.brand.replace(' ', '_'),
            "perfume": self.name.replace(' ', '_'),
            "card": os.path.abspath(f'./db/cards/{self.brand.replace(' ', '_')}_{self.name.replace(' ', '_')}.jpeg')
        }
        # self.f_id = None
        # self.f_score = None
        # self.f_accords = None
        # self.f_notes = None
        # self.f_card = os.path.abspath(f'./db/cards/{self.fragrantica["designer"]}_{self.fragrantica["perfume"]}')
        # self.f_link = f'https://www.fragrantica.com/perfume/{self.fragrantica["designer"]}/{self.fragrantica["perfume"]}-{self.fragrantica["id"]}.html'

    def get_fragrantica_details(self):
        return self.fragrantica

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

    