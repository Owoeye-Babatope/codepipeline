
import boto3
import sys
import json
import urllib
import uuid
import os
import time
import urllib.request
import typing
import psycopg2
psycopg2.paramstyle = 'named'
from botocore.errorfactory import ClientError
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
        options.add_argument("headless")
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
        self.connect()
        self.wait(10)
        self.driver.find_element(By.ID, "onetrust-accept-btn-handler").click()
    
    def search(self, x):
        '''This method searches for an input str in the website search bar
           The method does not return a value it only opens the search page
        '''
        self.accept_cookies()
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
            try:

                wines_xpath = '//*[@id="main-content"]/div[2]/div[3]/ul/li'
                wait = WebDriverWait(self.driver,20)
                wait.until(EC.presence_of_element_located((By.XPATH,wines_xpath)))
                return [self.driver.find_elements(By.XPATH, wines_xpath), wines_xpath]
            except:
                wines_xpath = '//*[@id="main-content"]/div[2]/div[2]/ul/li'
                wait = WebDriverWait(self.driver,20)
                wait.until(EC.presence_of_element_located((By.XPATH,wines_xpath)))
                return [self.driver.find_elements(By.XPATH, wines_xpath), wines_xpath]
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
        all_wines = self.get_all_wines()[0]
        if(len(all_wines) > 0):
            return len(all_wines)
        elif(len(all_wines) == 0):
            return 400


    def get_prod_details(self, wine: int):
        try:
            #print('\ncheck\n')
            #self.driver.implicitly_wait(5)

            all  = self.get_all_wines()
            all_wines = []
            if(len(all) > 0):
                all_wines = self.get_all_wines()[0]
            #wine_number = 18
            #all_wines[wine_number].click()
            all_wines[wine].click()
            self.wait(5)
            data = {}
            #self.wait(5)
            #print('\ncheck\n')
            #name_xpath = '//*[@id="overview"]/section[1]/header/h1/text()'

            
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
            
            self.driver.back()
            #self.driver.refresh()
            self.wait(3)
            return data
        except Exception as e:
            print(f'error occurred at for try level\n\n{e}')
            self.driver.back()
            #self.driver.refresh()
            self.wait(3)
            return {}
            
   

    def get_text_details(self, search_word: str):
        '''
        This mthod gets the details from each wine product.
        It also store the details as a json file alongside the iages of the product


        Improvements
            . Check the folders first for what data is available to avoid unnecessary opening the page to find that it exists already
            .
        '''

        s3 = boto3.resource('s3')
        s3c = boto3.client('s3')
        collection = {}
        # print(f"The Webpage title is {self.driver.title}")

        # Since we are interested in the wines available we find its link and click to get its page
        word_search = search_word
        self.search(word_search)
        self.wait(5)
        
        get_all_wines = self.get_all_wines()
        all_wines = get_all_wines[0]
        wines_xpath = get_all_wines[1]
        print(wines_xpath)
        number_of_wines = self.number_of_all_wines()
        # print(f"\nnumber of wines: {number_of_wines}\n")

        # We wait some 3 secs 
        self.wait(3)
        num = 0
        wine_name = ''
        try:
            parent_dir = f'{search_word}/'
            folder_name = os.path.join('./', parent_dir)
            os.mkdir(parent_dir)
        except:
            pass


        for wine in range(number_of_wines):
            wine_iter = wine + 1
            
            #all_wines = self.get_all_wines()
            class_name = ''
            try:
                class_name_xpath = f'{wines_xpath}[{wine_iter}]'
                self.scrolltoview(class_name_xpath)
                class_name = self.driver.find_element(By.XPATH, class_name_xpath).get_attribute('class')
            except:
                class_name_xpath = f'//*[@id="main-content"]/div[2]/div[2]/ul/li[{wine_iter}]'
                self.scrolltoview(class_name_xpath)
                class_name = self.driver.find_element(By.XPATH, class_name_xpath).get_attribute('class')
                
            if (class_name == 'fops-item fops-item--cluster' or class_name == 'fops-item fops-item--featured'):
                #print(class_name)
                name_pre_xpath = f'{class_name_xpath}/div[2]/div[1]/a/div[1]/div[2]/h4'
                name_of_wine = self.find_element_xpath(name_pre_xpath).text
                print(f'Name: {name_of_wine}, wine_number: {wine}')
                
                parent_dir = f'./{search_word}/'
                
                directory_name = name_of_wine + f'/'
                path = os.path.join(parent_dir, directory_name)
                
                try:

                    # s3_img_path = f'{search_word}/{name_of_wine}/images/{name_of_wine}.png'
                    # if it exists it runs successfully 
                    

                    # os.mkdir(path)
                    # file_path = path +'data.json'
                    # img_folder = '' # It needs to be defined at this level to be accessible outside the block
                    # try:
                    #     img_folder = path + 'images/'
                    #     os.mkdir(img_folder)
                    # except:
                    #     print('error occurred at image folder creation')
                    # print('\n here \n')
                    
                    img_folder = path + 'images/'
                    s3_img_path = f'{search_word}/{name_of_wine}/images/{name_of_wine}.png'
                    try:
                        s3c.head_object(Bucket='aicore-scrapped-data', Key= s3_img_path) # Confirm that the file exist in s3 else log it 
                        print(f'File originally existed')
                    except:
                        
                        store = self.get_prod_details(wine)
                        #print('\n here now \n')
                        if (len(store) > 0):

                            img_path = img_folder + f"{name_of_wine}.png"
                            (filename , header) = urllib.request.urlretrieve(store['img_link'])
                            #print('\n here \n'*2) 

                            data = open(filename, 'rb')
                            #print('\n here \n'*3)
                            s3.Bucket('aicore-scrapped-data').put_object(Key=s3_img_path, Body=data)

                            data = store
                            if not (self.check_data_exist_on_table(search_word, data)): # prevent code from relogging in sql
                                self.sql_(search_word, data) # log data in sql
                            obj = s3.Object('aicore-scrapped-data',f'{search_word}/{name_of_wine}/data.json') 
                            obj.put(Body=json.dumps(data))
                        #print(f'image and data uploaded successfully')
                        
                        # pass


                    #print(f'File originally existed')
                    # with open(file_path, 'w') as file:
                    #     stringed_file = json.dumps(store)
                    #     file.write(stringed_file) # use `json.loads` to do the reverse
                        
                except:
                    print(f'file exists for {name_of_wine} in s3 or folder')
                    continue
                    
                

    def close(self):
        print(f"Browser is closing")
        self.driver.close()


    def check_data_exist_on_table(self, table_name: str, data: dict):
        from sqlalchemy import create_engine, inspect, create_engine, MetaData, Table, Column, Integer, String, DateTime
        from sqlalchemy.orm import  declarative_base, sessionmaker
        from datetime import datetime

        HOST = 'aicore-postgres.cugn6azr5y0m.us-east-1.rds.amazonaws.com'
        USER = 'postgres_aicore'
        PASSWORD = 'postgres'
        DATABASE = 'postgres'
        PORT = 5432
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'
        
        joined_table_name = ''
        ii = ''
        if ' ' in table_name:
            splited_table_name = table_name.split(' ')
            for each in splited_table_name:
                joined_table_name = joined_table_name + each
        else:
            joined_table_name = table_name

        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=True)
        Session = sessionmaker(bind = engine)
        session = Session()
        data = data
        ii = str(data['item_id'])
        with engine.connect() as con: 
            # Get all data 
            #rs = con.execute(f"SELECT * FROM {joined_table_name} WHERE id = data['item_id']")
            
            # print(type(ii) == type('25f7489d-9bdf-465c-8703-1433aadba25c'))
            # ex = con.execute( f"SELECT EXISTS(SELECT 1 FROM {joined_table_name} WHERE id={ii})")        
            ex = con.execute(f"SELECT TRUE FROM {joined_table_name} WHERE id =  %(i)s LIMIT 1", {'i' : ii})        

            #print(ex)
            # for row in rs:
            #     print (row[0]) # print each id
            #     print('\n\n')
        return (ex.first()[0])


    def sql_(self, table_name: str, data: dict):
        from sqlalchemy import create_engine, inspect, create_engine, MetaData, Table, Column, Integer, String, DateTime
        from sqlalchemy.orm import  declarative_base, sessionmaker
        # import pandas as pd
        from datetime import datetime
        joined_table_name = ''
        
        if ' ' in table_name:
            splited_table_name = table_name.split(' ')
            for each in splited_table_name:
                joined_table_name = joined_table_name + each
        else:
            joined_table_name = table_name

        HOST = 'aicore-postgres.cugn6azr5y0m.us-east-1.rds.amazonaws.com'
        USER = 'postgres_aicore'
        PASSWORD = 'postgres'
        DATABASE = 'postgres'
        PORT = 5432
        DATABASE_TYPE = 'postgresql'
        DBAPI = 'psycopg2'

        engine = create_engine(f"{DATABASE_TYPE}+{DBAPI}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}", echo=True)
        Session = sessionmaker(bind = engine)
        session = Session()

        # with engine.connect() as con:            
        #             rs = con.execute('SELECT * FROM redwine')

        #             for row in rs:
        #                 print (row[0])
        #                 print('\n\n')
        # return rs

        Base = declarative_base()
        # print(f'\n\n\n\n{joined_table_name}\n\n\n\n')
        class Wine(Base):
            __tablename__ = joined_table_name
            
            id = Column(String(), primary_key=True)
            wine_name = Column(String()) 
            price = Column(String())
            country_of_origin = Column(String())
            alcohol_by_volume = Column(String())
            image_link = Column(String())
            description = Column(String())
            date_created = Column(DateTime(), default = datetime.utcnow)
        created = False
        
        try:
            # print(f'\n\ntry sql_   {joined_table_name}\n\n\n')
            Base.metadata.create_all(engine)
            created = True
        except:
            created = True
            
        if created:
            print('logging to sql ...')
            wine = Wine(
                id= data['item_id'],
                wine_name = data['name'],
                price = data['price'],
                description = data['description'],
                country_of_origin = data['country_of_origin'],
                alcohol_by_volume = data['alcoho_by_volume'],
                image_link = data['img_link'],
                )
            session.add(wine)
            '''
            from sqlalchemy.sql import text
            with engine.connect() as con:

                data = ( { "id": 1, "title": "The Hobbit", "primary_author": "Tolkien" },
                         { "id": 2, "title": "The Silmarillion", "primary_author": "Tolkien" },
                )

                statement = text("""INSERT INTO book(id, title, primary_author) VALUES(:id, :title, :primary_author)""")

                for line in data:
                    con.execute(statement, **line)



                with engine.connect() as con:            
                    rs = con.execute('SELECT * FROM book')

                    for row in rs:
                        print row

                Out[*]:
                (4, u'The Hobbit', u'Tolkien')
                (5, u'The Silmarillion', u'Tolkien')

        '''




            session.commit()
            print('logged on posgres')
        return ('logged')

if __name__ == '__main__':
    # sys.path.append('C:\\Users\\Sean Kelly\\Documents\\New folder (3)\\Data Science\\Aicore\\codepipeline')
    # from testt import test_scrapper as ts
    # print(os.path.dirname(os.getcwd()))
    # print(os.getcwd())








    # Let's use Amazon S3
    #data = open('Barefoot.png', 'rb')
    #s3.Bucket('aicore-scrapped-data').put_object(Key='Newfolder/test.jpg', Body=data)
    # s3 = boto3.client('s3')
    # res = s3.head_object(Bucket='aicore-scrapped-data', Key='Newfolder/test.jpg')
    # print(res)
    # data = {"item_id": "4d1642c3-ea8f-4505-ae71-eaeecc5baa5d", "name": "Barefoot Pinot Grigio 75cl", "price": "\u00a37", "description": "Barefoot Pinot Grigio is crisp and full of citrus and peach flavours. Goes well with chicken, seafood, spicy pasta and pizzas.", "country_of_origin": "Wine of California, U.S.A, Silver Medal 2014 Concours Mondial de Bruxelles U.S.A", "alcoho_by_volume": "12", "img_link": "https://www.ocado.com//productImages/641/64101011_0_640x640.jpg?identifier=4ff784e778fd588bd01679535d6a4c2d"}
    
    
    instance1 = Scrapper()

    instance1.get_text_details('red wine')
    instance1.close()
