import json
import os
import requests
import time
from typing import List, Dict
from bs4 import BeautifulSoup
from .cache import CacheService
from .models import Product
from .settings import settings


class ScraperService:
    def __init__(self, base_url: str, retry_count: int = 3, retry_delay: int = 5):
        self.base_url = base_url
        self.retry_count = retry_count
        self.retry_delay = retry_delay

    def fetch_page(self, url: str, proxy: str = None) -> str:
        for attempt in range(self.retry_count):
            try:
                proxies = {"http": proxy, "https": proxy} if proxy else None
                response = requests.get(url, proxies=proxies, timeout=10)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                print(f"Attempt {attempt + 1}/{self.retry_count} failed: {e}")
                if attempt < self.retry_count - 1:
                    time.sleep(self.retry_delay)
        raise Exception(f"Failed to fetch {url} after {self.retry_count} attempts.")

    def parse_products(self, html: str) -> List[Dict]:
        soup = BeautifulSoup(html, "html.parser")
        products = []

        product_cards = soup.select(".product-item")  # Adjust selector as per the website
        for card in product_cards:
            title = card.select_one(".product-title").text.strip()
            price = float(card.select_one(".price").text.strip().replace("$", ""))
            image_url = card.select_one(".product-image img")["src"]

            products.append({"title": title, "price": price, "image_url": image_url})

        return products

    def scrape(self, page_limit: int, proxy: str = None) -> List[Dict]:
        scraped_products = []

        for page in range(1, page_limit + 1):
            url = f"{self.base_url}?page={page}"
            print(f"Scraping page: {url}")
            html = self.fetch_page(url, proxy)
            products = self.parse_products(html)
            scraped_products.extend(products)

        return scraped_products


class StorageService:
    def __init__(self, file_path: str):
        self.file_path = file_path

    def load_data(self) -> List[Dict]:
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as f:
                return json.load(f)
        return []

    def save_data(self, products: List[Dict]):
        with open(self.file_path, "w") as f:
            json.dump(products, f, indent=4)

    def update_data(self, new_products: List[Dict], cache: CacheService) -> int:
        current_data = self.load_data()
        updated_data = []

        for product in new_products:
            cached_price = cache.get_price(product["title"])
            if cached_price is None or cached_price != product["price"]:
                cache.set_price(product["title"], product["price"])
                updated_data.append(product)

        current_data.extend(updated_data)
        self.save_data(current_data)
        return len(updated_data)


class NotificationService:
    @staticmethod
    def notify(status_message: str):
        print(f"Notification: {status_message}")


# Usage Example
if __name__ == "__main__":
    # Initialize services
    scraper = ScraperService(base_url="https://dentalstall.com/shop/")
    storage = StorageService(file_path="database.json")
    cache = CacheService(settings["CACHE_DB_URL"])
    notifier = NotificationService()

    # Configuration
    PAGE_LIMIT = 5
    PROXY = None

    # Scraping
    try:
        scraped_data = scraper.scrape(page_limit=PAGE_LIMIT, proxy=PROXY)
        updated_count = storage.update_data(scraped_data, cache)
        notifier.notify(f"Scraped {len(scraped_data)} products, updated {updated_count} in the database.")
    except Exception as e:
        notifier.notify(f"Scraping failed: {e}")
