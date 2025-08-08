import requests
import csv
import time
import json
from urllib.parse import quote
from dataclasses import dataclass
from typing import List, Optional
import logging
from dotenv import load_dotenv
import os


load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@dataclass
class Lead:
    """Data class to store lead information"""
    name: str
    address: str
    phone: Optional[str] = None
    website: Optional[str] = None
    rating: Optional[float] = None
    reviews_count: Optional[int] = None
    category: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class GoogleMapsLeadScraper:
    """Google Maps lead scraper using Google Places API (New)"""
    
    def __init__(self):
        # Hardcoded API key - replace with your actual key
        self.api_key = os.getenv('GOOGLE_MAPS_API_KEY')
        self.base_url = "https://places.googleapis.com/v1/places"
        self.session = requests.Session()
        self.session.timeout = 30
        self.leads: List[Lead] = []
        
        if not self.api_key:
            raise ValueError("Google Maps API key is required")
        
        # Set up headers for the new API
        self.session.headers.update({
            'Content-Type': 'application/json',
            'X-Goog-Api-Key': self.api_key,
            'X-Goog-FieldMask': 'places.displayName,places.formattedAddress,places.internationalPhoneNumber,places.websiteUri,places.rating,places.userRatingCount,places.types,places.location'
        })
    
    def search_places(self, query: str, location: str = "", max_results: int = 20) -> List[dict]:
        """Search for places using Google Places API"""
        url = f"{self.base_url}:searchText"
        
        search_query = f"{query} in {location}" if location else query
        
        request_body = {
            "textQuery": search_query,
            "maxResultCount": min(max_results, 20),
            "languageCode": "en"
        }
        
        if location:
            request_body["locationBias"] = {"regionCode": "US"}
        
        try:
            logger.info(f"Searching for: {search_query}")
            response = self.session.post(url, json=request_body)
            response.raise_for_status()
            return response.json().get('places', [])
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            if e.response:
                try:
                    error_data = e.response.json()
                    logger.error(f"API Error: {error_data}")
                except:
                    logger.error(f"Response status: {e.response.status_code}")
            return []
    
    def extract_lead_data(self, place: dict) -> Lead:
        """Extract lead data from API response"""
        display_name = place.get('displayName', {})
        name = display_name.get('text', '') if isinstance(display_name, dict) else str(display_name)
        
        return Lead(
            name=name,
            address=place.get('formattedAddress', ''),
            phone=place.get('internationalPhoneNumber') or place.get('nationalPhoneNumber'),
            website=place.get('websiteUri'),
            rating=place.get('rating'),
            reviews_count=place.get('userRatingCount'),
            category=', '.join(place.get('types', [])),
            latitude=place.get('location', {}).get('latitude'),
            longitude=place.get('location', {}).get('longitude')
        )
    
    def scrape_leads(self, query: str, location: str = "", max_results: int = 20) -> List[Lead]:
        """Main method to scrape leads"""
        if not query.strip():
            raise ValueError("Search query cannot be empty")
            
        logger.info(f"Starting scrape for '{query}' in '{location}'")
        
        places = self.search_places(query, location, max_results)
        leads = []
        
        for place in places:
            try:
                leads.append(self.extract_lead_data(place))
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                logger.error(f"Error processing place: {e}")
                continue
        
        self.leads = leads
        logger.info(f"Scraping completed. Found {len(leads)} leads")
        return leads