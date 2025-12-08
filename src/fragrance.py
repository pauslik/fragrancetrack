import os
from src.algolia import auto_search_fragrance
from src.fragrantica import download_fragrantica_card

class Fragrance():
    def __init__(self, 
                 brand: str, 
                 name: str, 
                 my_score: int = 0, 
                 card: str | None = None,
                 id: int | None = None, 
                 year: int | None = None, 
                 link: str | None = None):
        # required
        self.brand = brand
        self.name = name
        self.my_score = my_score
        # optional
        if card:
            self.card = card
        else:
            self.card = os.path.abspath(f'./db/cards/{self.brand.replace(' ', '_')}_{self.name.replace(' ', '_')}.jpeg')
        # get all fragrantica related details upon initialisation
        if id and year and link:
            self.id = id
            self.year = year
            self.link = link
        else:
            fragrantica = self._get_fragrantica_details()
            self.name = fragrantica["name"]
            self.id = fragrantica["id"]
            self.year = fragrantica["year"]
            self.link = fragrantica["link"]
        # download the card
        self._get_fragrantica_card()

    def _get_fragrantica_details(self):
        # result["brand"] = f_brand
        # result["name"] = f_name
        # result["id"] = f_id
        # result["link"] = f_link
        # result["year"] = f_year
        return auto_search_fragrance(self.brand, self.name)
    
    def _get_fragrantica_card(self):
        download_fragrantica_card(self.link, self.card, False)

    def __repr__(self) -> str:
        result = f'{self.brand} - {self.name} ({self.year})'
        # TODO use below conditions to append to the result based on existing values
        # if self.my_score != None:
        #     result += f'{result} {self.my_score}'
        return result
        
    def __eq__(self, other: object) -> bool:
        if isinstance(other, self.__class__):
            if self.brand == other.brand and self.name == other.name:
                return True
        return False

    