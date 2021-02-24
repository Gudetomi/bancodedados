import requests
from bs4 import BeautifulSoup as bs
import time
initial_time = time.time()
#coletando html da página
data = requests.get("https://www.freelancer.com/jobs/")
soup_data = bs(data.text, "html.parser")
current_page = 1
final_page = 200
Jobs = {}
cont = 0
contfreelas = 0
#iterando entre todas as páginas
while(current_page <= final_page):
    data = requests.get("https://freelancer.com/jobs/"  + str(current_page) + "/")
    soup_data = bs(data.text, "html.parser")
    #coletando nome, tags
    names = soup_data.find_all(class_="JobSearchCard-primary-heading-link")
    tags = soup_data.find_all(class_="JobSearchCard-primary-tags")
    bid = soup_data.find_all(class_="JobSearchCard-secondary-price")
    for i in names:
        #name
        treatedname = i.text.replace("    ", "")
        treatedname = treatedname.replace("\n", "")
        Jobs["name"] = treatedname
        #tags
        treatedtags = tags[cont].text.split('\n')
        for i in treatedtags:
            if i == "":
                treatedtags.remove(i)
        Jobs["tags"] = treatedtags
        #bid
        if "Private project" in treatedname:
            bid.insert(cont, "")
        if bid[cont]!= "":
            treatedbid = bid[cont].text.replace(" ", "")
            treatedbid = treatedbid.replace("\n", "")
            treatedbid = treatedbid.replace("AvgBid", "")
            Jobs["bid"] = treatedbid
        #site
        Jobs["site"] = "Freelancer"
        cont = cont + 1
        contfreelas = contfreelas + 1
        #fazer aqui a inserção no banco de dados
        #print(Jobs)
    print("CURRENT PAGE: ", current_page)
    current_page = current_page + 1
    cont=0

final_time = time.time()
print (contfreelas, " freelas encontrados")
print ("Tempo de execução:", final_time - initial_time)
