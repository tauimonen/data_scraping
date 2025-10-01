import requests
import os
from bs4 import BeautifulSoup

with open("index.html") as file:
    content = file.read()

soup = BeautifulSoup(content, "lxml")
h5 = soup.find_all("h5")
courses = soup.find_all("div", class_="card")

directory_name = "tau"

# Create a directory
try:
    os.mkdir(directory_name)
    print(f"Directory '{directory_name}' created successfully.")
except FileExistsError:
    print(f"Directory '{directory_name}' already exists.")
except PermissionError:
    print(f"Permission denied: Unable to create '{directory_name}'.")
except Exception as e:
    print(f"An error occurred: {e}")
    
# Write to the file
with open(f"{directory_name}/courses.txt", "w") as file:
    for c in courses:
        p = c.a.text.split()[-1]
        file.write(c.h5.text + " " + p + "\n")

## ctrl-ö = toggle terminal
# ctrl-k-c = kommentoi
# ctrl-k-u = pois