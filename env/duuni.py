import requests
from bs4 import BeautifulSoup
import pandas as pd
from tabulate import tabulate

url = "https://duunitori.fi/tyopaikat?haku=python"
response = requests.get(url)

if response.status_code == 200:
    html = response.text
    soup = BeautifulSoup(html, "lxml")
    
    jobs = soup.find_all(class_="gtm-search-result")
    job_list = []

    for job in jobs:
        title = job.text.strip()
        company = job.get("data-company")
        link = "https://duunitori.fi" + job.get("href") if job.get("href") else "Ei linkkiä"
        job_list.append({"Työpaikka": title, "Yhtiö": company, "Linkki": link})

    df = pd.DataFrame(job_list)
    print(tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False))
else:
    print("Sivua ei löytynyt", response.status_code)
