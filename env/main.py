import requests
from bs4 import BeautifulSoup

with open("index.html") as file:
    content = file.read()

soup = BeautifulSoup(content, "lxml")
h5 = soup.find_all("h5")
print(h5)
for item in h5:
    print(item)

list(map(print, h5))


""" url = "https://helsinginsuunnistajat.fi/"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
print(soup.prettify())


for i in soup.find_all('p'): 
    print(i.text.replace("\n", " ").strip()) """

## ctrl-ö = toggle terminal
# ctrl-k-c = kommentoi
# ctrl-k-u = pois