import requests
from bs4 import BeautifulSoup
import re
import math


def find_results_count(soup) -> int:
    """Finds the total number of results from a script tag"""
    for script in soup.find_all("script", string=True):
        match = re.search(r'"results_count":\s*"(\d+)"', script.string)
        if match:
            return int(match.group(1))
    return 0


def calculate_page_count(result_count: int, items_on_page: int = 20) -> int:
    return math.ceil(result_count / items_on_page)


def get_jobs_from_page(session, url: str):
    """Fetches job postings from a single page"""
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    return soup.find_all(class_="gtm-search-result")


def main():
    base_url = "https://duunitori.fi/tyopaikat"
    query = "?haku=python"

    with requests.Session() as session:
        # Fetch the first page
        resp = session.get(base_url + query)
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")

        result_count = find_results_count(soup)
        pages = calculate_page_count(result_count)

        print(f"Found {result_count} jobs, {pages} pages\n")

        printed_jobs = 0

        for i in range(1, pages + 1):
            url = f"{base_url}{query}&sivu={i}"
            jobs = get_jobs_from_page(session, url)

            for job in jobs:
                job_text = job.text.strip()
                company = job.get("data-company", "Unknown")
                link = "https://duunitori.fi" + job.get("href")
                print("-" * 50)
                print(f"Job: {job_text}\nCompany: {company}\nLink: {link}")
                printed_jobs += 1

        print(f"\nPrinted {pages} pages and {printed_jobs} jobs.")


if __name__ == "__main__":
    main()
