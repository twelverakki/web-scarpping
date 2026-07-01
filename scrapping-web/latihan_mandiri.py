"""
Latihan Mandiri - Web Scraping quotes.toscrape.com
Tugas:
1. Ambil semua kategori dari website quotes.toscrape
2. Ambil semua quote dari 3 halaman
3. Simpan hasil ke Excel
4. Tambahkan delay 2 detik tiap request
"""

import os
import time
import logging
from typing import List, Dict, Any
import requests
from bs4 import BeautifulSoup
import pandas as pd
from requests.adapters import HTTPAdapter
from urllib3.util import Retry

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


class QuotesScraper:
    """A professional scraper for quotes.toscrape.com.
    
    Uses connection pooling via requests.Session, includes automated retries,
    safely handles missing HTML tags, and exports data to Excel/CSV formats.
    """
    BASE_URL = "https://quotes.toscrape.com"
    HEADERS = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        )
    }

    def __init__(self, output_dir: str, delay: float = 2.0):
        self.output_dir = output_dir
        self.delay = delay
        self.session = self._init_session()

    def _init_session(self) -> requests.Session:
        """Initializes a requests Session with HTTP pooling and retries."""
        session = requests.Session()
        session.headers.update(self.HEADERS)
        retries = Retry(
            total=3,
            backoff_factor=1.0,
            status_forcelist=[500, 502, 503, 504],
            raise_on_status=False
        )
        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))
        return session

    def _get_soup(self, url: str) -> BeautifulSoup:
        """Fetches HTML from url and returns parsed BeautifulSoup object."""
        logging.info(f"Requesting page: {url}")
        try:
            response = self.session.get(url, timeout=10)
            time.sleep(self.delay)  # Delay between requests
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logging.error(f"Error requesting {url}: {e}")
            raise

    @staticmethod
    def _safe_extract_text(element, selector: str, default: str = "") -> str:
        """Safely extracts stripped text from BS4 element using CSS selector."""
        target = element.select_one(selector)
        return target.get_text(strip=True) if target else default

    def scrape_sidebar_tags(self) -> List[str]:
        """Scrapes the list of 'Top Ten tags' on the homepage sidebar."""
        try:
            soup = self._get_soup(f"{self.BASE_URL}/")
            tag_links = soup.select("div.tags-box a.tag")
            tags = [t.get_text(strip=True) for t in tag_links]
            logging.info(f"Successfully scraped {len(tags)} tags from sidebar.")
            return tags
        except Exception as e:
            logging.warning(f"Failed to scrape sidebar tags: {e}. Falling back to quote tags.")
            return []

    def scrape_quotes(self, max_pages: int = 3) -> List[Dict[str, Any]]:
        """Scrapes quotes, authors, and tags across the specified page range."""
        quotes = []
        for page in range(1, max_pages + 1):
            url = f"{self.BASE_URL}/page/{page}/"
            logging.info(f"Processing quotes page {page}/{max_pages}...")
            try:
                soup = self._get_soup(url)
                quote_divs = soup.select("div.quote")
                
                if not quote_divs:
                    logging.info(f"Page {page} is empty. Terminating pagination loop.")
                    break

                for div in quote_divs:
                    text = self._safe_extract_text(div, "span.text")
                    author = self._safe_extract_text(div, "small.author")
                    tags = [t.get_text(strip=True) for t in div.select("a.tag")]

                    quotes.append({
                        "halaman": page,
                        "quote": text,
                        "penulis": author,
                        "tags": ", ".join(tags)
                    })
            except Exception as e:
                logging.error(f"Failed to scrape quotes on page {page}: {e}")
                # Continue scraping other pages if one fails
                continue
                
        return quotes

    def save_results(self, quotes: List[Dict[str, Any]], sidebar_tags: List[str]):
        """Exports quotes and categories to Excel (.xlsx) if openpyxl is installed,
        otherwise gracefully falls back to CSV format.
        """
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Consolidate and sort unique categories/tags
        all_tags = set(sidebar_tags)
        for q in quotes:
            if q["tags"]:
                for tag in q["tags"].split(", "):
                    all_tags.add(tag)
        sorted_tags = sorted(list(all_tags))

        df_quotes = pd.DataFrame(quotes)
        df_categories = pd.DataFrame({"kategori": sorted_tags})

        excel_path = os.path.join(self.output_dir, "quotes_data.xlsx")
        csv_quotes_path = os.path.join(self.output_dir, "quotes.csv")
        csv_categories_path = os.path.join(self.output_dir, "kategori.csv")

        try:
            # Attempt to write to Excel (requires openpyxl)
            with pd.ExcelWriter(excel_path, engine="openpyxl") as writer:
                df_quotes.to_excel(writer, sheet_name="Quotes", index=False)
                df_categories.to_excel(writer, sheet_name="Categories", index=False)
            logging.info(f"Successfully saved combined data to Excel: {excel_path}")
        except ImportError:
            logging.warning("Python library 'openpyxl' is missing. Saving as CSV instead.")
            df_quotes.to_csv(csv_quotes_path, index=False)
            df_categories.to_csv(csv_categories_path, index=False)
            logging.info(f"Saved quotes to: {csv_quotes_path}")
            logging.info(f"Saved categories to: {csv_categories_path}")
            logging.info("Tip: Run 'pip install openpyxl' to enable Excel (.xlsx) exports.")


def main():
    # Resolve the directory paths dynamically based on script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(workspace_dir, "output", "latihan-mandiri")

    logging.info("=== Starting Latihan Mandiri Scraper ===")
    
    scraper = QuotesScraper(output_dir=output_dir, delay=2.0)
    
    # Task 1: Get sidebar tags
    sidebar_tags = scraper.scrape_sidebar_tags()
    
    # Task 2: Get all quotes from 3 pages
    quotes_data = scraper.scrape_quotes(max_pages=3)
    
    logging.info(f"Scraped {len(quotes_data)} quotes and {len(sidebar_tags)} sidebar categories.")
    
    # Task 3 & 4: Save findings (with 2s delay between requests implemented in _get_soup)
    scraper.save_results(quotes_data, sidebar_tags)
    
    logging.info("=== Latihan Mandiri Scraper Completed ===")


if __name__ == "__main__":
    main()
