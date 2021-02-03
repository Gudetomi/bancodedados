#Teste
import requests
from bs4 import BeautifulSoup

page = requests.get("https://www.freelancer.com/jobs/")

if page.status_code == 200:
    print("Página baixada com sucesso!!")
    
soup = BeautifulSoup(page.content, 'html.parser')
print(soup.prettify())
