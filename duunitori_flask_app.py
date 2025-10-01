from flask import Flask, request, render_template_string, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re
import math

app = Flask(__name__)

# --- template ---
TEMPLATE = (
    TEMPLATE
) = """
<!DOCTYPE html>
<html lang="fi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Työpaikat – {{ query }}</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 2rem; background: #f9f9f9; }
        h1 { color: #333; }
        .search-box { margin-bottom: 1.5rem; }
        input[type=text] {
            padding: 0.5rem;
            width: 250px;
            border: 1px solid #ccc;
            border-radius: 6px;
            margin-right: 0.5rem;
        }
        button {
            padding: 0.5rem 1rem;
            border: none;
            background-color: #007bff;
            color: white;
            border-radius: 6px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        .search-info { margin-bottom: 1rem; color: #666; }
        ul { list-style-type: none; padding: 0; }
        li { background: #fff; margin: 0.5rem 0; padding: 1rem; border-radius: 8px;
             box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        a { text-decoration: none; color: #007bff; font-weight: bold; }
        a:hover { text-decoration: underline; }
        .company { color: #555; font-size: 0.9em; margin-top: 0.3rem; }
    </style>
</head>
<body>
    <h1>Työpaikat</h1>
    
    <div class="search-box">
        <form method="get" action="/">
            <input type="text" name="q" placeholder="Hakusana..." value="{{ query }}">
            <button type="submit">Hae</button>
        </form>
    </div>

    <div class="search-info">
        Löytyi yhteensä <strong>{{ total_jobs }}</strong> työpaikkaa (näytetään max {{ pages }} sivua).
    </div>
    
    <ul>
        {% for job in jobs %}
        <li>
            <a href="{{ job.link }}" target="_blank">{{ job.text }}</a>
            <div class="company">{{ job.company }}</div>
        </li>
        {% endfor %}
    </ul>
</body>
</html>
"""


# --- helper functions ---
def find_results_count(soup) -> int:
    for script in soup.find_all("script", string=True):
        match = re.search(r'"results_count":\s*"(\d+)"', script.string)
        if match:
            return int(match.group(1))
    return 0


def calculate_page_count(result_count: int, items_on_page: int = 20) -> int:
    return math.ceil(result_count / items_on_page)


def get_jobs_from_page(session, url: str):
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    return soup.find_all(class_="gtm-search-result")


# --- Flask routes ---
@app.route("/")
def index():
    query = request.args.get("q", "python")
    base_url = "https://duunitori.fi/tyopaikat"
    query_param = f"?haku={query}"

    with requests.Session() as session:
        resp = session.get(base_url + query_param)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            return f"Failed to fetch search page: {resp.status_code}", 500

        soup = BeautifulSoup(resp.text, "lxml")
        total_jobs = find_results_count(soup)
        pages = calculate_page_count(total_jobs)

        max_pages_to_scrape = min(pages, 5)
        jobs_out = []

        for i in range(1, max_pages_to_scrape + 1):
            page_url = f"{base_url}{query_param}&sivu={i}"
            elems = get_jobs_from_page(session, page_url)
            for e in elems:
                text = e.text.strip()
                company = e.get("data-company", "Unknown")
                href = e.get("href") or ""
                link = "https://duunitori.fi" + href if href.startswith("/") else href
                jobs_out.append({"text": text, "company": company, "link": link})

    return render_template_string(
        TEMPLATE, jobs=jobs_out, total_jobs=total_jobs, pages=pages, query=query
    )


if __name__ == "__main__":
    app.run(debug=True)
