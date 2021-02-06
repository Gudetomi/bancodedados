import requests
from bs4 import BeautifulSoup as bs
import time
initial_time = time.time()
#coletando html da página
data = requests.get("https://www.guru.com/d/jobs/")
soup_data = bs(data.text, "html.parser")

#encontrando o número da última página
pages = soup_data.find(id="ctl00_guB_ulpaginate")
pages_string = str(pages.contents[-1])
final_page = []
for i in pages_string:
    if i.isdigit():
        final_page.append(i)
final_page= int("".join(list(final_page)))

#iterando entre todas as páginas
current_page = 1
while (current_page <= final_page):
    data = requests.get("https://www.guru.com/d/jobs/" + "pg/" + str(current_page) + "/")
    soup_data = bs(data.text, "html.parser")
    freelas = soup_data.find_all(class_="jobRecord__title")
    #for i in freelas:
    #    print(i.text)
    current_page = current_page + 1;
final_time = time.time()
print ("Tempo de execução:", final_time-initial_time)