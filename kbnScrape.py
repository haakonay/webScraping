########## IMPORTS ##########
import requests                          # Requests for requesting and downloading URLs
from bs4 import BeautifulSoup, Comment   # For parsing downloaded URLs
import re                                # Regular Expressions
from collections import Counter          # For returning most common words in dictionary
import validators                        # Validating URLs provided by user
from validators import ValidationFailure # -
import time                              # For providing the user with time spent and for testing

url_kommuner = "https://snl.no/kommuner_i_Norge"
url = "https://opengov.360online.com/Meetings/"

downloaded_page = requests.get(url_kommuner)
soup_downloaded_page = BeautifulSoup(downloaded_page.text, features="html.parser")
print(soup_downloaded_page.findAll('td'))

