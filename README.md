# Duunitori Job Search Scraper (Flask)

A simple **Flask-based web application** that scrapes job postings from [Duunitori.fi](https://duunitori.fi) and displays them in a Bootstrap-powered interface.

The app fetches the total number of results, calculates the number of pages, and lists job postings from the first few pages.

⚠️ **Note:** This project is for demonstration and educational purposes only. Please use responsibly and follow the target site’s terms of service.

## Features

- Search jobs by keyword (default: `python`)
- Fetch and display the total number of results and pages
- Scrape job postings from the first 5 pages
- Clean UI with [Bootstrap 5](https://getbootstrap.com/)
- Display job description snippet, company name, and direct link to posting

## Tech Stack

- [Python 3.10+](https://www.python.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Requests](https://docs.python-requests.org/)
- [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [Bootstrap 5](https://getbootstrap.com/)

## Installation

1. **Clone the repository and navigate into it**:

   ```bash
   # Clone the repository
   git clone https://github.com/your-username/duunitori-flask-scraper.git

   # Change directory into the cloned folder
   cd duunitori-flask-scraper
   
2. Create a virtual environment and install dependencies:

   ```bash
  python -m venv .venv
  source .venv/bin/activate   # Linux/macOS
  .venv\Scripts\activate      # Windows

  pip install -r requirements.txt
  ```
  Example requirements.txt:
  
  flask
  requests
  beautifulsoup4
  lxml

3. Run the application:
  ```bash
   python duunitori_flask_app.py
```
4. Open your browser at:
   http://127.0.0.1:5000

## Usage

- Enter a search keyword (e.g., data engineer) in the search bar

- Press Search to see results

- Each job card shows:

    - Short job description

    - Company name

    - Link to the posting on Duunitori

## Author

  Created by TAU 2025

S  imple demo project combining Flask + Web Scraping
