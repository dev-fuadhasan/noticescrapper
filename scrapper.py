import requests
from bs4 import BeautifulSoup
from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

class NoticeScraper:
    def __init__(self):
        self.url = "https://daffodilvarsity.edu.bd/noticeboard"
        self.headers = {
            'User-Agent': 'Mozilla/5.0'
        }

    def parse_date(self, date_text):
        """Convert date text to ISO format"""
        for suffix in ["th", "st", "nd", "rd"]:
            date_text = date_text.replace(suffix, "")
        try:
            return datetime.strptime(date_text.strip(), "%d %B %Y").isoformat()
        except:
            return None

    def scrape_notices(self):
        try:
            response = requests.get(self.url, headers=self.headers)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')

            notices = []
            notice_items = soup.find_all('div', class_='row full-notice mb-2')

            for item in notice_items:
                try:
                    link_element = item.find('a', class_='noticeFile')
                    title = link_element.text.strip() if link_element else "No Title"
                    link = link_element.get('onclick', '')

                    if 'myFunction' in link:
                        notice_id = link.split('(')[1].split(',')[0]
                        link = f"https://daffodilvarsity.edu.bd/notice/{notice_id}"
                    else:
                        link = "#"

                    department_div = item.find('div', class_='col-md-5')
                    department = department_div.text.strip() if department_div else "General"

                    date_div = item.find('div', class_='col-md-3')
                    date_text = date_div.text.strip() if date_div else "No Date"
                    iso_date = self.parse_date(date_text)

                    notices.append({
                        'title': title,
                        'link': link,
                        'department': department,
                        'date': date_text,
                        'timestamp': iso_date
                    })

                except Exception as e:
                    continue

            return notices

        except requests.RequestException:
            return []

# API
app = FastAPI()

# CORS for Android app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/notices")
def get_notices():
    scraper = NoticeScraper()
    return {"notices": scraper.scrape_notices()}
