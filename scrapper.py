
import sys
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

chrome_options = Options()


class Scrapper:
    def __init__(self):
        options = Options()
        options.add_argument("no-sandbox")
        # options.add_argument("headless")
        options.add_argument("start-maximized")
        #options.add_argument("window-size=1900,1080");
        #chrome_options.add_argument("--headless")
        #options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.web_address = "https://www.ocado.com/"
    
    def connect(self):
        self.driver.get(self.web_address)

    def accept_cookies(self):
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    
    def search(self, x):
        try:
            search_bar_xpath = '//*[@id="findText"]' 
            search_box = self.driver.find_element(By.XPATH, search_bar_xpath)
            search_box.send_keys(x)

            search_xpath = '//*[@id="findButton"]'
            search = self.driver.find_element(By.XPATH, search_xpath).click()
        except:
            print('Error occurred: Could not search')
            self.driver.close()
            sys.exit('Exited')


    def wait(self, x):
        #a
        self.driver.implicitly_wait(x)

    def find_element_xpath(self, x):
        return self.driver.find_element(By.ID, x)

    def get_elem_attr(self, elem, iter, attr):
        return str(elem[iter].get_attribute(attr))

    def get_all_wines(self):
        try:
            wines_xpath = '//*[@id="main-content"]/div[2]/div[3]/ul/li'
            return self.driver.find_elements(By.XPATH, wines_xpath)
        except:
            print('could not get all')
            self.driver.close()
            sys.exit('Excited')

    def get_with_multi(self, a_xpath, b_xpath):
        try: 
            return self.driver.find_element(By.XPATH, a_xpath).text
        except:
            print('\nNone of the xpath are visible\n')
            return self.driver.find_element(By.XPATH, b_xpath).text


    def get(self):
        collection = {}
        print(f"The Webpage title is {self.driver.title}")

        # Wait some 10 secs for the page to load its contents
        self.wait(10)
        # Find the accept button to accept cookies and hence clear the dialog box
        self.accept_cookies()
        # Wait some 3 secs for all to be set
        self.wait(3)
        # Since we are interested in the wines available we find its link and click to get its page
        word_search = 'red wine'
        self.search(word_search)

        self.wait(5)

        print(f"\nnumber of wines:\n")
        
        wines_xpath = '//*[@id="main-content"]/div[2]/div[3]/ul/li'
        all_wines = self.get_all_wines()

        number_of_wines = len(all_wines)
        print(f"\nnumber of wines: {number_of_wines}\n")

        # We wait some 3 secs 
        self.wait(3)
        num = 0
        for wine_number in range(number_of_wines):
            all_wines = self.get_all_wines()
            if (self.get_elem_attr(all_wines, wine_number, 'id') == ''):
                try:
                    #self.driver.implicitly_wait(5)
                    all_wines = self.get_all_wines()
                    #wine_number = 18
                    all_wines[wine_number].click()
                    data = {}
                    self.wait(5)
                    
                    name_xpath = '//*[@id="overview"]/section[1]/header/h2'
                    wine_name = self.find_element_xpath(name_xpath).text

                    price_xpath = '//*[@id="overview"]/section[2]/div[1]/div/h2'
                    wine_price = self.find_element_xpath(price_xpath).text

                    description_xpath = '//*[@id="productInformation"]/div[2]/div[1]/div[2]/div/div[1]/div'
                    wine_description = self.find_element_xpath(description_xpath).text

                    a_country_xpath = '//*[@id="productInformation"]/div[2]/div[1]/div[2]/div/div[3]/div'    
                    b_country_xpath = '//*[@id="overview"]/section[1]/header/h2'
                    country_of_origin = self.get_with_multi(a_country_xpath, b_country_xpath)
                    
                    try:
                        ABV_xpath = '//*[@id="productInformation"]/div[3]/div/div[2]/div[2]/div/div[1]/div'
                        ABV_percentage = self.driver.find_element(By.XPATH, ABV_xpath).text
                    except:
                        ABV_xpath = '//*[@id="productInformation"]/div[3]/div/div/div[2]/div/div[1]/div'
                        ABV_percentage = self.driver.find_element(By.XPATH, ABV_xpath).text  
                    
                    expand_brand_xpath = '//*[@id="productInformation"]/div[2]/div[3]/div[1]/div/button'
                    #self.driver.find_element(By.XPATH, expand_brand_xpath).click()
                    #manufacturer_xpath = '//*[@id="productInformation"]/div[2]/div[3]/div[2]/div/div[2]/div'
                    #'//*[@id="productInformation"]/div[2]/div[3]/div[2]/div/div/div'

                    #manufacturer = self.driver.find_element(By.XPATH, manufacturer_xpath).text
                    self.driver.implicitly_wait(3)
                    data['name'] = wine_name
                    data['price'] = wine_price
                    data['description'] = wine_description
                    data['country_of_origin'] = country_of_origin
                    data['alcoho_by_volume'] = ABV_percentage
                    #data['manufacturer'] = manufacturer
                    print(f"\n{num} {wine_name}\n")
                    collection[num] = data
                    num += 1
                    self.driver.back()
                    # self.driver.implicitly_wait(3)
                except:
                    print('error occurred at for try level')
                    collection[num] = 'Error Occurred while logging'
                    continue
        with open('collected_data.txt', 'w') as file:
            file.write(json.dumps(collection))

        print(collection)
        #elementName = self.driver.findElement(By.ID("topNav_Wine Sale"))

        '''
        search_bar = self.driver.find_element_by_name("q")
        search_bar.clear()
        search_bar.send_keys("getting started with python")
        search_bar.send_keys(Keys.RETURN)
        '''
    def close(self):
        print(f"Browser is closing")
        self.driver.close()


if __name__ == '__main__':
    scrap = Scrapper()
    
    
    scrap.connect()
    scrap.get()
    scrap.close()
