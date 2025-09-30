from flask import Flask, request, render_template_string, redirect, url_for
import requests
from bs4 import BeautifulSoup
import re
import math

app = Flask(__name__)

# --- helper functions ---

def find_results_count(soup) -> int:
    """Finds the total number of results from a script tag."""
    for script in soup.find_all("script", string=True):
        match = re.search(r'"results_count":\s*"(\d+)"', script.string)
        if match:
            return int(match.group(1))
    return 0


def calculate_page_count(result_count: int, items_on_page: int = 20) -> int:
    """Calculates how many pages are required given items per page."""
    return math.ceil(result_count / items_on_page)


def get_jobs_from_page(session, url: str):
    """Fetches job postings from a single page and returns a list of job elements."""
    resp = session.get(url)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "lxml")
    return soup.find_all(class_="gtm-search-result")


# --- Flask routes ---

TEMPLATE = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Duunitori jobs</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
  </head>
  <body class="bg-light">
    <div class="container py-4">
      <h1 class="mb-3">Duunitori job search</h1>

      <form method="get" action="/">
        <div class="input-group mb-3">
          <input name="q" value="{{ query }}" class="form-control" placeholder="search term">
          <button class="btn btn-primary" type="submit">Search</button>
          <a class="btn btn-secondary ms-2" href="{{ url_for('index') }}">Default</a>
        </div>
      </form>

      <p>Found <strong>{{ total_jobs }}</strong> jobs across <strong>{{ pages }}</strong> pages.</p>

      <div class="mb-3">
        <a class="btn btn-outline-primary" href="{{ url_for('index', q=query) }}">Refresh</a>
      </div>

      {% for job in jobs %}
      <div class="card mb-2">
        <div class="card-body">
          <h5 class="card-title">{{ job.text[:120] }}{% if job.text|length > 120 %}...{% endif %}</h5>
          <p class="card-text">Company: <strong>{{ job.company }}</strong></p>
          <a href="{{ job.link }}" class="card-link" target="_blank">Open on Duunitori</a>
        </div>
      </div>
      {% endfor %}

      <footer class="pt-4 text-muted">Created by TAU 2025, Simple scraper + Flask demo. Use responsibly and follow site terms.</footer>
    </div>
  </body>
</html>
"""


@app.route('/')
def index():
    """Main page: scrape Duunitori for the given query and show results."""
    query = request.args.get('q', 'python')
    base_url = "https://duunitori.fi/tyopaikat"
    query_param = f"?haku={query}"

    with requests.Session() as session:
        # fetch first page to learn total count
        resp = session.get(base_url + query_param)
        try:
            resp.raise_for_status()
        except requests.HTTPError:
            return f"Failed to fetch search page: {resp.status_code}", 500

        soup = BeautifulSoup(resp.text, "lxml")
        total_jobs = find_results_count(soup)
        pages = calculate_page_count(total_jobs)

        # collect jobs from first few pages to avoid very long scrapes
        max_pages_to_scrape = min(pages, 5)
        jobs_out = []

        for i in range(1, max_pages_to_scrape + 1):
            page_url = f"{base_url}{query_param}&sivu={i}"
            elems = get_jobs_from_page(session, page_url)
            for e in elems:
                text = e.text.strip()
                company = e.get('data-company', 'Unknown')
                href = e.get('href') or ''
                link = 'https://duunitori.fi' + href if href.startswith('/') else href
                jobs_out.append({
                    'text': text,
                    'company': company,
                    'link': link
                })

    return render_template_string(TEMPLATE, jobs=jobs_out, total_jobs=total_jobs, pages=pages, query=query)


if __name__ == '__main__':
    # Run the app on localhost:5000
    app.run(debug=True)
