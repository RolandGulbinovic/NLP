from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from IPython.display import HTML
import fasttext.util
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_colwidth', None)
from scraping import get_markes, get_modeliai, get_category, get_detales
from GUI import GUI
global mark_list, mark_title

#fasttext.util.download_model('lt', if_exists='ignore') # vektorius lietuvisku zodziu
ft = fasttext.load_model('cc.lt.300.bin')

mark_title, mark_list = get_markes()

GUI(mark_list, mark_title, ft)
