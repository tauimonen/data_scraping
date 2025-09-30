import requests
import os
from bs4 import BeautifulSoup

with open("index.html") as file:
    content = file.read()

soup = BeautifulSoup(content, "lxml")
h5 = soup.find_all("h5")
courses = soup.find_all("div", class_="card")


for c in courses:
    course_name = c.h5.text
    parts = c.a.text.split(" ")
    price = parts[2]


directory_name = "tau"

try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")
    
with open("tau/courses.txt", "w") as file:
    for c in courses:
        p = c.a.text.split()[-1]
        file.write(c.h5.text + " " + p + "\n")
    
texts = [h5.get_text() for h5 in soup.find_all('h5', class_='card-title')]
#list(map(print, texts))


""" url = "https://helsinginsuunnistajat.fi/"
req = requests.get(url)
soup = BeautifulSoup(req.text, "html.parser")
print(soup.prettify())


for i in soup.find_all('p'): 
    print(i.text.replace("\n", " ").strip()) """

## ctrl-ö = toggle terminal
# ctrl-k-c = kommentoi
# ctrl-k-u = pois