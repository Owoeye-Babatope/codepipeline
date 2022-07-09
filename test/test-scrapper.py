import unittest
#import pydantic
import Restructure
from Restructure import Scrapper
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

    def test_get_prod_details(self):
        Scrap = Scrapper()
        Scrapper.search(Scrap, 'red wine')
        output = type(Scrapper.get_prod_details(Scrap, 0))
        print(output)
        self.assertEqual(output, type({}))
    






if __name__ == '__main__':
    unittest.main()