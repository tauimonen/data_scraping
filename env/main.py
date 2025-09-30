import requests
from bs4 import BeautifulSoup

url = "https://helsinginsuunnistajat.fi/"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
print(soup.prettify())


for i in soup.find_all('p'): 
    print(i.text.replace("\n", " ").strip())
