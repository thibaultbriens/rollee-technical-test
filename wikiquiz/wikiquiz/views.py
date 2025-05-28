import json
from django.http import JsonResponse
from django.views import View

from .scraper_wikipedia import WikipediaScraper

class Quiz(View):
    def get(self, request, *args, **kwargs):
        scraper = WikipediaScraper()
    
        url = request.GET.get("url", "https://en.wikipedia.org/wiki/Python_(programming_language)")
        print(f"Url: {url}")
        
        result = scraper.scrape_wikipedia_page(url)
        
        if result != None:
            title, all_paragraphs = result

            responseData = {
                "title": title,
                "paragraphs": all_paragraphs
            }
            
            return JsonResponse(responseData)

    