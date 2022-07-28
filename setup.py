from setuptools import setup
from setuptools import find_packages

setup(
    name='Selenium_Wine_detail_Scrapper', ## This will be the name your package will be published with
    version='0.0.1', 
    description='This package contains a main scrapper file for scrapping the ocado web',
    url='https://github.com/Owoeye-Babatope/codepipeline.git', # Add the URL of your github repo if published 
                                                                   # in GitHub
    author='Owoeye Babatope', # Your name
    license='MIT',
    packages=find_packages(), # This one is important to explain. See the notebook for a detailed explanation
    install_requires=['requests', 'beautifulsoup4'], # For this project we are using two external libraries
                                                     # Make sure to include all external libraries in this argument
)