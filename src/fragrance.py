import os
from src.algolia import search_algolia
from src.fragrantica import download_fragrantica_card

class Fragrance():
    def __init__(self, brand: str, name: str, my_score: int | None = None):
        # required
        self.brand = brand
        self.name = name
        # optional
        self.my_score = my_score
        # generated
        # self.file_brand = self.brand.replace(' ', '_')
        # self.file_name = self.name.replace(' ', '_')
        # self.link_brand = self.brand.replace(' ', '-')
        # self.link_name = self.name.replace(' ', '-')
        self.card = os.path.abspath(f'./db/cards/{self.brand.replace(' ', '_')}_{self.name.replace(' ', '_')}.jpeg')
        # get all fragrantica related details upon initialisation
        fragrantica = self._get_fragrantica_details()
        self.id = fragrantica["id"] 
        self.year = fragrantica["year"]
        self.link = fragrantica["link"]

        # download the card
        self._get_fragrantica_card()

    def _get_fragrantica_details(self):
        return search_algolia(self.brand, self.name)
    
    def _get_fragrantica_card(self):
        download_fragrantica_card(self.link, self.card)

    def __repr__(self) -> str:
        result = f'{self.brand} - {self.name} ({self.year})'
        if self.my_score != None:
            result += f'{result} {self.my_score}'

        return result
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            if self.brand == other.brand and self.name == other.name:
                return True
        return False

    