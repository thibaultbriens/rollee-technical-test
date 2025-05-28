from playwright.sync_api import sync_playwright
import time
import random

def main():
    with sync_playwright() as p:
        # Launch browser with additional options
        browser = p.chromium.launch(
            headless=False,  # Visible browser is less suspicious
            slow_mo=random.randint(50, 100)  # Random timing between actions
        )
        
        # Create a more human-like browser context
        context = browser.new_context(
            viewport={'width': random.randint(1200, 1600), 'height': random.randint(700, 900)},
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36',
            locale='fr-FR',
            timezone_id='Europe/Paris',
            geolocation={'longitude': 4.8357, 'latitude': 45.7640},
            permissions=['geolocation'],
            has_touch=False,
            is_mobile=False
        )
        
        page = context.new_page()

        # To look like a human
        page.mouse.move(random.randint(100, 500), random.randint(100, 500))
        
        try:
            extract_reviews(page, "brasserie-georges-lyon")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            page.screenshot(path="error_screenshot.png")
            browser.close()


def extract_reviews(page, restaurant: str):
    # First visit Yelp homepage and search naturally
    try:
        print("Visiting Yelp homepage...")
        page.goto("https://www.yelp.com/", timeout=60000, wait_until="domcontentloaded")
        
        human_like_delay()
        
        # Search for the restaurant naturally
        if page.locator('input[name="find_desc"]').count() > 0:
            print("Searching for the restaurant...")
            page.fill('input[name="find_desc"]', restaurant)
            human_like_delay()
            page.press('input[name="find_loc"]', 'Enter')
            
            # Wait for search results
            page.wait_for_selector('.business-name', timeout=60000)
            human_like_delay()
            
            # Click on the restaurant link
            page.click('.business-name')
        else:
            # If search form not found, try direct navigation
            print("Search form not found, trying direct navigation...")
            page.goto(url, timeout=90000, wait_until="domcontentloaded")
    except Exception as e:
        print(f"Initial navigation failed: {e}")
        print("Trying direct navigation...")
        page.goto(url, timeout=90000, wait_until="domcontentloaded")
    
    # Wait for the page to load
    print("Waiting for page content to load...")
    try:
        page.wait_for_selector("h1", timeout=60000)
        human_like_delay()
        
        # Scroll down a bit like a human would
        for _ in range(3):
            page.mouse.wheel(0, random.randint(300, 700))
            human_like_delay(min_delay=1, max_delay=3)
        
        # Now try to find the reviews section
        print("Looking for reviews section...")
        # Click on reviews tab if not already there
        if page.locator('a[href*="reviews"]').count() > 0:
            page.click('a[href*="reviews"]')
            human_like_delay()
        
        # Extract business name
        try:
            business_name = page.locator("h1").first.inner_text()
            print(f"Business name: {business_name}")
        except Exception as e:
            print(f"Could not extract business name: {e}")
        
        # Extract some reviews as proof of concept
        review_elements = page.locator('.review__09f24__oHr9V').all()
        print(f"Found {len(review_elements)} reviews")
        
        for i, review in enumerate(review_elements[:3]):  # Just get first 3 for demo
            try:
                rating = review.locator('.rating-star').get_attribute('aria-label')
                text = review.locator('.comment__09f24__gu0rG').inner_text()
                print(f"Review {i+1}: {rating}")
                print(f"Text: {text[:100]}...")  # First 100 chars
                human_like_delay()
            except Exception as e:
                print(f"Error extracting review {i+1}: {e}")
        
    except Exception as e:
        print(f"Error during page interaction: {e}")
        page.screenshot(path=f"error_during_extraction.png")


def human_like_delay(min_delay=0.5, max_delay=2.5):
    """Add random delay to mimic human behavior"""
    time.sleep(random.uniform(min_delay, max_delay))


if __name__ == "__main__":
    main()