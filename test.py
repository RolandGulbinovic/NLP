from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from IPython.display import HTML


from scraping import get_markes, get_modeliai, get_category, get_detales
from GUI import GUI
global mark_list, mark_title
aaaa
mark_title, mark_lisst = get_markes()
GUI(mark_list, mark_title)
