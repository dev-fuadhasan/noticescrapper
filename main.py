# main.py
from flask import Flask, jsonify
from scraper import NoticeScraper

app = Flask(__name__)
scraper = NoticeScraper()

@app.route('/notices', methods=['GET'])
def get_notices():
    # Fetch notices using the scraper
    notices = scraper.scrape_notices()
    return jsonify(notices), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
