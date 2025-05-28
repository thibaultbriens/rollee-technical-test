import requests
from bs4 import BeautifulSoup
import re

class WikipediaScraper:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def scrape_wikipedia_page(self, url):
        """Extract all paragraphs from Wikipedia page"""
        try:
            response = self.session.get(url)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Page title
            title = soup.find('h1', {'class': 'firstHeading'}).get_text()
            
            # Content div
            content_div = soup.find('div', {'class': 'mw-content-ltr mw-parser-output'})
            
            all_paragraphs = []
            
            # Get all <p>
            all_elements = content_div.find_all(['p'])
            
            for element in all_elements:
                if element.name == 'p':
                    text = element.get_text().strip()
                    if text:
                        # Check if text has at least 15 words, to be relevant
                        if (len(text.split(' ')) < 15):
                            continue

                        # Remove link references in brackets [1], [2], etc.
                        text = re.sub(r'\[\d+\]', '', text)
                        all_paragraphs.append(text)
            
            return title, all_paragraphs
            
        except Exception as e:
            print(f'Error scraping page: {str(e)}')
            return None
    
    def save_paragraphs_to_file(self, title, all_paragraphs, filename=None):
        """Save all paragraphs to a text file"""
        if not filename:
            safe_title = re.sub(' ', '_', title)
            filename = f"{safe_title}_paragraphs.txt"
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"Wikipedia Page: {title}\n")
                f.write("=" * 50 + "\n\n")
                
                for i, paragraph in enumerate(all_paragraphs, 1):
                    f.write(paragraph + "\n\n")
            
            print(f"Paragraphs saved to: {filename}")
            return True
            
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            return False

'''if __name__ == "__main__":
    scraper = WikipediaScraper()
    
    # Example URL
    url = "https://en.wikipedia.org/wiki/Python_(programming_language)"
    
    result = scraper.scrape_wikipedia_page(url)
    
    if result != None:
        title, all_paragraphs = result
        
        # Save to file
        scraper.save_paragraphs_to_file(title, all_paragraphs)'''