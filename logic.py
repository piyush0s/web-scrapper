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
    """
    Google Maps lead scraper using Google Places API
    Note: This requires a Google Places API key for production use
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key
        self.base_url = "https://maps.googleapis.com/maps/api/place"
        self.session = requests.Session()
        self.leads: List[Lead] = []
        
    def search_places(self, query: str, location: str = "", radius: int = 5000) -> List[dict]:
        """
        Search for places using Google Places API Text Search
        
        Args:
            query: Search query (e.g., "restaurants", "dentist")
            location: Location to search around (e.g., "New York, NY")
            radius: Search radius in meters
        """
        if not self.api_key:
            logger.error("API key required for Google Places API")
            return []
            
        url = f"{self.base_url}/textsearch/json"
        params = {
            'query': f"{query} in {location}" if location else query,
            'key': self.api_key,
            'radius': radius
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data.get('results', [])
            else:
                logger.error(f"API Error: {data['status']}")
                return []
                
        except requests.RequestException as e:
            logger.error(f"Request failed: {e}")
            return []
    
    def get_place_details(self, place_id: str) -> Optional[dict]:
        """Get detailed information for a specific place"""
        if not self.api_key:
            return None
            
        url = f"{self.base_url}/details/json"
        params = {
            'place_id': place_id,
            'key': self.api_key,
            'fields': 'name,formatted_address,formatted_phone_number,website,rating,user_ratings_total,geometry,types'
        }
        
        try:
            response = self.session.get(url, params=params)
            response.raise_for_status()
            data = response.json()
            
            if data['status'] == 'OK':
                return data.get('result', {})
            else:
                logger.error(f"Details API Error: {data['status']}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Details request failed: {e}")
            return None
    
    def scrape_leads(self, query: str, location: str = "", max_results: int = 20) -> List[Lead]:
        """
        Main method to scrape leads from Google Maps
        
        Args:
            query: What to search for (e.g., "restaurants", "auto repair")
            location: Where to search (e.g., "Chicago, IL")
            max_results: Maximum number of results to return
        """
        logger.info(f"Starting scrape for '{query}' in '{location}'")
        
        # Search for places
        places = self.search_places(query, location)
        
        if not places:
            logger.warning("No places found")
            return []
        
        # Limit results
        places = places[:max_results]
        
        leads = []
        for i, place in enumerate(places, 1):
            logger.info(f"Processing place {i}/{len(places)}: {place.get('name', 'Unknown')}")
            
            # Get detailed information
            place_id = place.get('place_id')
            details = self.get_place_details(place_id) if place_id else {}
            
            # Create lead object
            lead = Lead(
                name=place.get('name', ''),
                address=place.get('formatted_address', ''),
                phone=details.get('formatted_phone_number'),
                website=details.get('website'),
                rating=place.get('rating'),
                reviews_count=place.get('user_ratings_total'),
                category=', '.join(place.get('types', [])),
                latitude=place.get('geometry', {}).get('location', {}).get('lat'),
                longitude=place.get('geometry', {}).get('location', {}).get('lng')
            )
            
            leads.append(lead)
            
            # Be respectful with API calls
            time.sleep(0.1)
        
        self.leads = leads
        logger.info(f"Scraping completed. Found {len(leads)} leads")
        return leads
    
    def export_to_csv(self, filename: str = "leads.csv") -> None:
        """Export scraped leads to CSV file"""
        if not self.leads:
            logger.warning("No leads to export")
            return
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = [
                'name', 'address', 'phone', 'website', 
                'rating', 'reviews_count', 'category', 
                'latitude', 'longitude'
            ]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for lead in self.leads:
                writer.writerow({
                    'name': lead.name,
                    'address': lead.address,
                    'phone': lead.phone or '',
                    'website': lead.website or '',
                    'rating': lead.rating or '',
                    'reviews_count': lead.reviews_count or '',
                    'category': lead.category or '',
                    'latitude': lead.latitude or '',
                    'longitude': lead.longitude or ''
                })
        
        logger.info(f"Leads exported to {filename}")

# Alternative scraper using web scraping (use with caution)
class WebScrapingGoogleMaps:
    """
    Web scraping approach - USE WITH EXTREME CAUTION
    This may violate Google's Terms of Service
    """
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def search_and_scrape(self, query: str, location: str = ""):
        """
        WARNING: This method may violate Google's ToS
        Consider using the API approach instead
        """
        logger.warning("Web scraping approach - use at your own risk!")
        # Implementation would go here but is not recommended
        pass

def main():
    """Example usage of the Google Maps Lead Scraper"""
    
    # You need to get a Google Places API key from Google Cloud Console
    API_KEY = "YOUR_GOOGLE_PLACES_API_KEY_HERE"
    
    # Initialize scraper
    scraper = GoogleMapsLeadScraper(api_key=API_KEY)
    
    # Example: Scrape restaurants in New York
    leads = scraper.scrape_leads(
        query="restaurants",
        location="New York, NY",
        max_results=10
    )
    
    # Export to CSV
    scraper.export_to_csv("restaurant_leads.csv")
    
    # Print summary
    print(f"\nScraping Summary:")
    print(f"Total leads found: {len(leads)}")
    
    for lead in leads[:3]:  # Show first 3 leads
        print(f"\nBusiness: {lead.name}")
        print(f"Address: {lead.address}")
        print(f"Phone: {lead.phone or 'N/A'}")
        print(f"Rating: {lead.rating or 'N/A'}")

if __name__ == "__main__":
    main()