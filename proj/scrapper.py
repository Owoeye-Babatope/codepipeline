
import sys
import json
import urllib
import uuid
import os
import time
import urllib.request
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC


class Scrapper:
    '''This Scrapper Class scraps data from a chosen website using the Selenium module and methods.


        Example
        --------

            scrap = Scrapper()
    

        Note
        ----
            This class is specially created for the "https://www.ocado.com/" websites as every website has got different feature which making them unique hence requiring a unique approach to scrapping.

        Methods
        -------

        connect()
        accept_cookies()
        search()
        navigate()
        wait()
        find_element_xpath()
        get_elem_attr()
        get_all_wines()
        get_with_multi()
    '''
    def __init__(self):
        '''
        This initialises the options for the browser instance.
        It could also be used to initialize some private variables of the scrapper class such as login details for some logins.
        
            Function parameters should be documented in the ``Args`` section. The name
    of each parameter is required. The type and description of each parameter
    is optional, but should be included if not obvious.

    If \*args or \*\*kwargs are accepted,
    they should be listed as ``*args`` and ``**kwargs``.

    The format for a parameter is::

        name (type): description
            The description may span multiple lines. Following
            lines should be indented. The "(type)" is optional.

            Multiple paragraphs are supported in parameter
            descriptions.

    Args:
        param1 (int): The first parameter.
        param2 (:obj:`str`, optional): The second parameter. Defaults to None.
            Second line of description should be indented.
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.

    Returns:
        bool: True if successful, False otherwise.

        The return type is optional and may be specified at the beginning of
        the ``Returns`` section followed by a colon.

        The ``Returns`` section may span multiple lines and paragraphs.
        Following lines should be indented to match the first line.

        The ``Returns`` section supports any reStructuredText formatting,
        including literal blocks::

            {
                'param1': param1,
                'param2': param2
            }

    Raises:
        AttributeError: The ``Raises`` section is a list of all exceptions
            that are relevant to the interface.
        ValueError: If `param2` is equal to `param1`.
        
        '''

        options = Options()
        #options.add_argument("headless")
        #options.add_argument("window-size=1900,1080")
        options.add_argument("no-sandbox")
        options.add_argument("start-maximized")
        self.driver = webdriver.Chrome(chrome_options=options)
        self.web_address = "https://www.ocado.com/"
    
    def connect(self):
        '''
        This method calls the get method to connect to the initialized website
        '''
        self.driver.get(self.web_address)

    def accept_cookies(self):
        '''This method simply accepts the cookies option'''
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    
    def search(self, x):
        '''This method searches for an input str in the website search bar
           The method does not return a value it only opens the search page
        '''

        try:
            search_bar_xpath = '//*[@id="findText"]'
            wait = WebDriverWait(self.driver,60)
            wait.until(EC.presence_of_element_located((By.XPATH,search_bar_xpath)))
            search_box = self.driver.find_element(By.XPATH, search_bar_xpath)
            search_box.send_keys(x)
            print('\nSearching...\n')
            search_xpath = '//*[@id="findButton"]'
            search = self.driver.find_element(By.XPATH, search_xpath).send_keys(Keys.RETURN)
            self.wait(2)
        except Exception as e:
            print('Error occurred: Could not search')
            #pass
            self.driver.close()
            #sys.exit('Exited')

    def wait(self, x):
        '''This method is used to make the selenium driver implicitily wait to the input time in seconds'''
        self.driver.implicitly_wait(x)

    def find_element_xpath(self, x):
        '''This method only searches for only one web element based on the input xpath
           The method is able to wait for the path for 60 secs before it raises an error if it is not found else it returns the element
        '''
        wait = WebDriverWait(self.driver,60)
        wait.until(EC.presence_of_element_located((By.XPATH,x)))
        return self.driver.find_element(By.XPATH, x)

    def get_all_wines(self):
        '''This method gets all wine elements on the page after a search action
            It returns a list of elements and if unsuccessful it returns an empty list 
        '''

        try:
            wines_xpath = '//*[@id="main-content"]/div[2]/div[3]/ul/li'
            wait = WebDriverWait(self.driver,60)
            wait.until(EC.presence_of_element_located((By.XPATH,wines_xpath)))
            return self.driver.find_elements(By.XPATH, wines_xpath)
        except Exception as e:
            print(f'could not get the wine list retrying...\n {e}')
            self.driver.refresh()
            self.wait(5)
            return []
            

    def get_with_multi(self, a_xpath: str, b_xpath: str):
        '''This method gets element from a web page from either of the xpaths provided'''

        try: 
            return self.driver.find_element(By.XPATH, a_xpath).text
        except:
            return self.driver.find_element(By.XPATH, b_xpath).text

    def scrolltoview(self, xpath):
        '''This method brings the element which is to be interacted with to view.
            It only accepts the xpath of the element.
        '''
        element = self.driver.find_element(By.XPATH, xpath)
        actions = ActionChains(self.driver)
        actions.move_to_element(element).perform()


    def number_of_all_wines (self):
        '''This method gets all the wines instances on the page and returns its len 
        if it fails a default value of 400 is returned
        '''
        all_wines = self.get_all_wines()
        if(len(all_wines) > 0):
            return len(all_wines)
        elif(len(all_wines) == 0):
            return 400


    def get_text_details(self):
        '''
        This mthod gets the details from each wine product.
        It also store the details as a json file alongside the iages of the product


        Improvements
            . Check the folders first for what data is available to avoid unnecessary opening the page to find that it exists already
            .
        '''
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

        number_of_wines = self.number_of_all_wines()
        print(f"\nnumber of wines: {number_of_wines}\n")

        # We wait some 3 secs 
        self.wait(3)
        num = 0
        wine_name = ''
        for wine in range(number_of_wines):
            wine_iter = wine + 1
            print(f'Total number of wines: {number_of_wines}, wine_number: {wine}')
            all_wines = self.get_all_wines()
            
            class_name_xpath = f'//*[@id="main-content"]/div[2]/div[3]/ul/li[{wine_iter}]'
            self.scrolltoview(class_name_xpath)
            class_name = self.driver.find_element(By.XPATH, class_name_xpath).get_attribute('class')
            if (class_name == 'fops-item fops-item--cluster'):
                try:
                    #print('\ncheck\n')
                    #self.driver.implicitly_wait(5)
                    all_wines = self.get_all_wines()
                    #wine_number = 18
                    #all_wines[wine_number].click()
                    all_wines[wine].click()
                    self.wait(5)
                    data = {}
                    #self.wait(5)
                    #print('\ncheck\n')
                    

                    name_xpath = '//*[@id="overview"]/section[1]/header/h1'
                    self.scrolltoview(name_xpath)
                    wait = WebDriverWait(self.driver,5)
                    wait.until(EC.presence_of_element_located((By.XPATH,name_xpath)))
                    #print('\ncheck\n')
                    #self.scrolltoview(name_xpath)
                    wine_name = self.find_element_xpath(name_xpath).text
                    #wine_name = 'Wine'
                    #print('\ncheck\n')
                    price_xpath = '//*[@id="overview"]/section[2]/div[1]/div/h2'
                    wine_price = self.find_element_xpath(price_xpath).text
                    #print('\ncheck\n')
                    description_xpath = '//*[@id="productInformation"]/div[2]/div[1]/div[2]/div/div[1]/div'
                    wine_description = self.find_element_xpath(description_xpath).text
                    #print('\ncheck\n')
                    a_country_xpath = '//*[@id="productInformation"]/div[2]/div[1]/div[2]/div/div[2]/div'    
                    b_country_xpath = '//*[@id="overview"]/section[1]/header/h2'
                    
                    country_of_origin = self.get_with_multi(a_country_xpath, b_country_xpath)
                    #country_of_origin = 'check'
                    try:
                        ABV_xpath = '//*[@id="productInformation"]/div[3]/div/div[2]/div[2]/div/div[1]/div'
                        ABV_percentage = self.driver.find_element(By.XPATH, ABV_xpath).text
                    except:
                        ABV_xpath = '//*[@id="productInformation"]/div[3]/div/div/div[2]/div/div[1]/div'
                        ABV_percentage = self.driver.find_element(By.XPATH, ABV_xpath).text  
                    
                    #Get image link
                    img_xpath = '//*[@id="overview"]/section[1]/div/div/div[1]/img'
                    src = self.driver.find_element(By.XPATH, img_xpath)
                    img_link = 'https://www.ocado.com/' + str(src.get_attribute('src'))
                    
                    print(img_link)
                    expand_brand_xpath = '//*[@id="productInformation"]/div[2]/div[3]/div[1]/div/button'

                    uid = str(uuid.uuid4())
                    #print(uid)
                    data['item_id'] = f'{uid}'
                    data['name'] = wine_name
                    data['price'] = wine_price
                    data['description'] = wine_description
                    data['country_of_origin'] = country_of_origin
                    data['alcoho_by_volume'] = ABV_percentage
                    data['img_link'] = img_link
                    collection[wine_name] = data
                    

                    store = {f'{wine_name}':data}
                    #print(store)
                    parent_dir = './raw_data/'
                    directory_name = wine_name + f'/'
                    path = os.path.join(parent_dir, directory_name)
                    try:
                        os.mkdir(path)
                        file_path = path +'data.json'
                        img_folder = ''
                        try:
                            img_folder = path + 'images/'
                            os.mkdir(img_folder)
                        except:
                            print('error occurred at image folder creation')
                    
                        img_path = img_folder + f"{wine_name}.png"
                        urllib.request.urlretrieve(img_link, img_path) 


                        print(file_path)
                        with open(file_path, 'w') as file:
                            stringed_file = json.dumps(store)
                            file.write(stringed_file) # use `json.loads` to do the reverse

                    except:
                        print('file exists')

                    self.driver.back()
                    #self.driver.refresh()
                    self.wait(3)

                except Exception as e:
                    print(f'error occurred at for try level\n\n{e}')
                    collection[wine_name] = 'Error Occurred while logging'
                    self.driver.back()
                    self.driver.refresh()
                    self.wait(3)
                    continue

    def close(self):
        print(f"Browser is closing")
        self.driver.close()


if __name__ == '__main__':
    instance1 = Scrapper()
    
    #instance1.get_images()
    instance1.connect()
    instance1.get_text_details()
    instance1.close()
