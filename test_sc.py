import unittest
import os
import sys

# os.chdir(os.path.dirname(sys.path[0]))
#import pydantic

# append the path of the
# parent directory
# sys.path.append("..")
# print(sys.path[0])
# print(os.getcwd())
from main import Scrapper
'''     connect()
        accept_cookies()
        search()
        navigate()
        wait()
        find_element_xpath()
        get_elem_attr()
        get_all_wines()
        get_with_multi()
        
'''


class TestScrapper(unittest.TestCase):
      
    def est_connect(self):
        Scrap = Scrapper()
        self.assertIsNone(Scrapper.connect(Scrap))
    
    def est_accept_cookies(self):
        Scrap = Scrapper()   
        self.assertIsNone(Scrapper.accept_cookies(Scrap))
       
    def est_search(self):
        Scrap = Scrapper()    
        self.assertIsNone(Scrapper.search(Scrap, 'wine'))

    def est_get_prod_details(self):
        Scrap = Scrapper()
        Scrapper.search(Scrap, 'red wine')
        output = type(Scrapper.get_prod_details(Scrap, 0))
        print(output)
        self.assertEqual(output, type({}))

    def test_sql_(self):
        Scrap = Scrapper()
        table_name = 'red wine'
        data = {
        "item_id": "25f7489d-9bdf-465c-8703-1433aadba25c",
        "name": "Barefoot Pinot Grigio 75cl",
        "price": "\u00a37", 
        "description": "Barefoot Pinot Grigio is crisp and full of citrus and peach flavours. Goes well with chicken, seafood, spicy pasta and pizzas.", 
        "country_of_origin": "Wine of California, U.S.A, Silver Medal 2014 Concours Mondial de Bruxelles U.S.A", 
        "alcoho_by_volume": "12", 
        "img_link": "https://www.ocado.com//productImages/641/64101011_0_640x640.jpg?identifier=4ff784e778fd588bd01679535d6a4c2d"
        }
        output = Scrapper.sql_(Scrap, table_name, data)
        self.assertEqual(output, 'logged')

if __name__ == '__main__':
    unittest.main()