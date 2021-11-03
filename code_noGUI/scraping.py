# Markes
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from IPython.display import HTML

# metodas gauti visas markes
def get_markes():
    page = requests.get("https://rrr.lt/")
    soup = BeautifulSoup(page.content, 'html.parser')

    mark_list = soup.find(class_ ="cars_list clearfix")
#mark_list = soup.find_all(class_ = "cars_list__links")
    mark_list = mark_list.select(".cars_list__items a.cars_list__links")

    mark_title ={ list(mark_list[sd].children)[0][:-1]:mark_list[sd]["href"] for sd in range(len(mark_list))}

    markes = pd.DataFrame({
        "Markes": mark_title.items(),
    })
    mark_list = []
    for key, value in mark_title.items():
        mark_list.append(key)
    
    return mark_title, mark_list # mark_title - biblioteka{marke: nuoroda}, mark_list - list(marke)


# metodas, gauti visus modelius
def get_modeliai(x, marks):
    mark_title = marks
    page = requests.get(mark_title[x])
    soup = BeautifulSoup(page.content, 'html.parser')
    models_list = soup.find(class_="models_hold")
#print(models_list.prettify())
#model_title = [sd.get_text() for sd in models_list.select(".models .model-title")]
    models_list = models_list.select(".models .models__links")

    model_title ={ models_list[sd]['data-label']:models_list[sd]["href"] for sd in range(len(models_list))}
    
    model_list = []
    for key, value in model_title.items():
        model_list.append(key)
        
    return model_title, model_list # model_title - biblioteka{modelis: nuoroda}, model_list - list(modelis)

# Metodas, gauti kategorijas ir kieki
def get_category(x, models):
    model_title = models
    page = requests.get(model_title[x])
    soup = BeautifulSoup(page.content, 'html.parser')

    parts = soup.find(class_ = "parts")
    parts = parts.find_all(class_ = "parts__text")
# parts_link = soup.find_all(class_ = "parts_all-categories")
    parts_links = soup.select(".parts_all-categories a")
    parts_title ={list(parts[sd].children)[0][:-1].replace('\n                    ', '')+" >> "+str(list(parts[sd].children)[1].get_text()):parts_links[sd]["href"] for sd in range(len(parts))}

    raktai = []
    for key, value in parts_title.items():
        if re.search("Šioje kategorijoje dalių neturime", key):
            key = re.sub("Šioje kategorijoje dalių neturime", "(0)", key)
        raktai.append(key)
        
 # Read Note below
    
    return parts_title, raktai # parts_title - biblioteka{kategorija: nuoroda}, raktai - list(kateogorijos)

# gauti tos kategorijos prekes
def get_detales(x, marke, parts):
    parts_title = parts
    parts_spec = []
    parts_detales = []
    last = True
    next_ = parts_title[x]
    while(last):
        page = requests.get(next_)
        soup = BeautifulSoup(page.content, 'html.parser')
    
        page_last = soup.find(class_ = "pages__items last") 
        page_last = page_last.find(class_ = "pages__links")
    
        if page_last["class"] == ["pages__links"]:
            next_ = page_last["href"]
        else:
            last = False
        
        parts_details =soup.select(".products__text p")
        parts_specs = soup.select(".products .products__image")
        parts_price = soup.select(".products .products__price")
    
        parts_spec += [parts_specs[sd]["title"] + " " + parts_specs[sd]["href"] + " " +  parts_price[sd].get_text() for sd in range(len(parts_specs))]
    
        parts_detales += [parts_details[sd].get_text() for sd in range(len(parts_details))]
    
    a = 0

    item = []
    links = []
    kainos = []

    url =  "(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})"
    
    # sukuriami list'ai, kuriuos idedu i  pandas df
    for i in range(len(parts_spec)):
        x = re.search(".+?(?=https:)", parts_spec[i])
        y = re.search(url, parts_spec[i])
        item.append(x.group())
        links.append(y.group())
        e = parts_spec[i].split()[-1]
        k = parts_spec[i].split()[-2]
        price = e + k
        kainos.append(price)
    
    
    
    detales_info = [i for i in parts_detales if i.startswith(marke)]

    detales = pd.DataFrame({
        "Detalė": item,
        "Kaina": kainos, 
        "Info": detales_info,
        "Nuoroda": links,
    })
    detales_info_list = []
    
    for inp in range(len(detales)):
        pasirinkta_preke = detales.loc[inp, 'Nuoroda']

        page = requests.get(pasirinkta_preke)
        soup = BeautifulSoup(page.content, 'html.parser')

        detailed_info = soup.select(".product_desc .product_details")

        detailed_test = [sd.get_text() for sd in soup.select(".product_desc .product_details")]
        detailed_test = re.sub("\n", "|", detailed_test[1])
        detailed_test = detailed_test.split("|")
        
        del detailed_test[detailed_test == '']
        detales_info_dict = {}
        detales_info_list2 = []
        k = 0
        
        detales_info_list.append(detailed_test)
   
    detales["daugiau_info"] = detales_info_list
    
    return detales