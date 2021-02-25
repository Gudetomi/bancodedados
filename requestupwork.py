# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup as bs
import time
import datetime
import re
initial_time = time.time()

#extraindo links de cada categoria
def extract_source(url):
    agent = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0'}
    source=requests.get(url, headers=agent).text
    return source

def extract_data(source):
    cat = 0
    soup = bs(source, 'lxml')
    return soup
    
Links = []
Categories = []
soup_data = extract_data(extract_source('https://www.upwork.com/freelance-jobs/'))
links = soup_data.findAll(class_="vs-link-text")
for i in links:
    Links.append(i.get('href'))
    category = i.text.replace("   ", "")
    category = category.replace("\n", "")
    category = category.replace("Jobs", "")
    Categories.append(category)
cp = 0
cont = 0
contjobs = 0
current_page = "https://www.upwork.com" + Links[cp]
#iterando entre todas as páginas

while(current_page != "https://www.upwork.com" + Links[-1]):
    soup_data = extract_data(extract_source(current_page))
    #coletando dados específicos
    names = soup_data.find_all(class_="vs-color-avocado")
    tags = soup_data.find_all(class_="skills-list")
    date = soup_data.find_all(class_="pb-20")
    bid = soup_data.select(".job-tile-content .row")
    for i in names:
        Jobs = {}
        #name
        Jobs['name'] = i.text
        #category
        Jobs['category'] = Categories[cp]
        #tags
        treatedtags = tags[cont].text.replace("  ", "")
        treatedtags = treatedtags.replace(" Jobs", "")
        treatedtags = treatedtags.split('\n')
        for i in treatedtags:
            if i == "":
                treatedtags.remove(i)
        Jobs['tags'] = treatedtags
        #bid
        regexbid = re.compile(r'\${1}(\d+)')
        treatedbid = regexbid.search(bid[cont].text)
        if treatedbid != None:
            Jobs['bid'] = treatedbid.group()
        #date
        treateddate = date[cont].text.replace("&dash; ", "")
        treateddate = treateddate.replace("Fixed-price ","")
        treateddate = treateddate.replace("Hourly ","")
        Jobs['date'] = treateddate
        #site
        Jobs['site'] = "Upwork"
        #fazer aqui a inserção no banco de dados
        print(Jobs)
        cont = cont + 1
        contjobs = contjobs + 1    
    print("CURRENT PAGE: ", cp+1)
    #próxima página
    time.sleep(10)
    cont = 0
    cp = cp + 1
    current_page = "https://www.upwork.com" + Links[cp]
print("Total de jobs coletados:", contjobs)
final_time = time.time()
print ("Tempo de execução:", final_time - initial_time)
