from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from .services import ScraperService, StorageService, NotificationService
from .cache import CacheService
from .auth import authenticate
from .settings import settings

# Initialize FastAPI app
app = FastAPI(title="Web Scraper API")

# Initialize services
scraper = ScraperService(base_url="https://dentalstall.com/shop/")
storage = StorageService(file_path="database.json")
cache = CacheService(settings["CACHE_DB_URL"])
notifier = NotificationService()


@app.post("/scrape", dependencies=[Depends(authenticate)])
async def scrape(
    page_limit: int = Query(5, description="Number of pages to scrape"),
    proxy: str = Query(None, description="Proxy URL for scraping")
):
    """
    Scrape product data from the website and store it in the database.
    
    Args:
        page_limit (int): Number of pages to scrape.
        proxy (str): Proxy URL to use for requests.

    Returns:
        JSONResponse: Summary of scraping results.
    """
    try:
        # Scrape the data
        scraped_data = scraper.scrape(page_limit=page_limit, proxy=proxy)

        # Update storage
        updated_count = storage.update_data(scraped_data, cache)

        # Notify results
        summary = {
            "scraped_products": len(scraped_data),
            "updated_products": updated_count,
            "status": "success"
        }
        notifier.notify(f"Scraped {len(scraped_data)} products, updated {updated_count} in the database.")
        return JSONResponse(content=summary, status_code=200)

    except Exception as e:
        error_message = f"Scraping failed: {e}"
        notifier.notify(error_message)
        raise HTTPException(status_code=500, detail=error_message)


@app.get("/")
async def health_check():
    """
    Health check endpoint to verify that the service is running.
    """
    return {"status": "ok", "message": "Web scraper service is up and running!"}
