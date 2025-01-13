# Scraping-Tool
A scraping tool using Python FastAPI framework to automate the information scraping process from the target.

1. Scrape the product name, price, and image from each page of the catalogue.
Different settings can be provided as input, so your tool should be able to recognize them and work accordingly. For the current task, you can implement only two optional settings:
    1. The first one will limit the number of pages from which we need to scrape the information (for example, `5` means that we want to scrape only products from the first 5 pages).
    2. The secod one will provide a proxy string that tool can use for scraping
       
2. Store the scraped information in a database. For simplicity, you can store it on your PC's local storage as a JSON file format.

3. At the end of the scraping cycle, you need to notify designated recipients about the scraping status - send a simple message that will state how many products were scraped and updated in DB during the current session. 

Guidelines:

- Ensure type validation and data integrity using appropriate methods. Remember, accurate typing is crucial for data validation and processing efficiency.
- Consider adding a simple retry mechanism for the scraping part.
- Add simple authentication to the endpoint using a static token.
- Add a scraping results caching mechanism using your favourite in-memory DB. If the scraped product price has not changed, we don’t want to update the data of such a product in the DB.

## Project Usage

### Clone the repository:

`git clone <repo-url>
cd scraper_tool`

### Install dependencies:

`pip install -r requirements.txt`

### Start the application:

`uvicorn app.main:app --reload`

### Use the /scrape endpoint with POST:

`{
  "page_limit": 5,
  "proxy": "http://your-proxy-server:port"
}
`
