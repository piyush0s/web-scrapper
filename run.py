from flask import Flask, render_template, request, jsonify
from logic import GoogleMapsLeadScraper
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor
import logging

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
executor = ThreadPoolExecutor(max_workers=4)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.route('/')
def home():
    """Render the main scraper interface"""
    return render_template('home.html')

@app.route('/scrape', methods=['POST'])
def scrape():
    """API endpoint for scraping leads"""
    data = request.json
    
    # Validate required fields
    if not data or 'query' not in data:
        return jsonify({'error': 'Missing required fields'}), 400
    
    # Extract parameters
    query = data['query']
    location = data.get('location', '')
    max_results = min(int(data.get('maxResults', 20)), 200)  # Cap at 200
    
    try:
        # Run scraping in background thread
        future = executor.submit(run_scraper, query, location, max_results)
        leads = future.result()
        
        return jsonify({
            'success': True,
            'leads': leads,
            'stats': {
                'total': len(leads),
                'with_phone': sum(1 for lead in leads if lead.get('phone')),
                'with_website': sum(1 for lead in leads if lead.get('website')),
            }
        })
    except Exception as e:
        logger.error(f"Scraping failed: {str(e)}")
        return jsonify({'error': str(e)}), 500

def run_scraper(query, location, max_results):
    """Run the scraper and return leads as dictionaries"""
    scraper = GoogleMapsLeadScraper()
    leads = scraper.scrape_leads(query, location, max_results)
    return [lead.__dict__ for lead in leads]

if __name__ == '__main__':
    # Run with production settings
    app.run(host='0.0.0.0', port=5000, threaded=True)