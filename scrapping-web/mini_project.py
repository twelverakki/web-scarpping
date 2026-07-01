"""
Mini Project - Web Scraping scrapethissite.com/pages/
Scrape 3 halaman, masing-masing disimpan ke file CSV terpisah:
1. Countries of the World: A Simple Example
2. Hockey Teams: Forms, Searching and Pagination
3. Oscar Winning Films: AJAX and Javascript
"""

import os
import time
import json
import logging
from typing import List, Dict, Any, Optional
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


class ScrapeThisSiteScraper:
    """A professional scraper for scrapethissite.com.
    
    Includes simple HTML parsing, form-pagination, and AJAX JSON endpoints.
    Employs connection pooling (requests.Session), automatic retries,
    robust tag selectors, and proper error management.
    """
    BASE_URL = "https://www.scrapethissite.com"
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

    def _get_soup(self, url: str, params: Optional[Dict[str, Any]] = None) -> BeautifulSoup:
        """Fetches HTML from url and returns parsed BeautifulSoup object."""
        logging.info(f"Requesting HTML: {url} with params {params or {}}")
        try:
            response = self.session.get(url, params=params, timeout=10)
            time.sleep(self.delay)  # Delay between requests
            response.raise_for_status()
            return BeautifulSoup(response.text, "html.parser")
        except requests.RequestException as e:
            logging.error(f"Error requesting HTML {url}: {e}")
            raise

    def _get_json(self, url: str, params: Optional[Dict[str, Any]] = None) -> Any:
        """Fetches JSON response from url and parses it."""
        logging.info(f"Requesting JSON: {url} with params {params or {}}")
        try:
            response = self.session.get(url, params=params, timeout=10)
            time.sleep(self.delay)  # Delay between requests
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f"Error requesting JSON {url}: {e}")
            raise
        except json.JSONDecodeError as e:
            logging.error(f"Invalid JSON returned from {url}: {e}")
            raise

    @staticmethod
    def _safe_extract_text(element, selector: str, default: str = "") -> str:
        """Safely extracts stripped text from BS4 element using CSS selector."""
        target = element.select_one(selector)
        return target.get_text(strip=True) if target else default

    def scrape_countries(self) -> pd.DataFrame:
        """1. Scrapes country listings from scrapethissite.com/pages/simple/."""
        url = f"{self.BASE_URL}/pages/simple/"
        logging.info("Starting scrape: Countries of the World")
        
        try:
            soup = self._get_soup(url)
            countries = []
            
            country_divs = soup.select("div.country")
            for div in country_divs:
                negara = self._safe_extract_text(div, "h3.country-name")
                ibukota = self._safe_extract_text(div, "span.country-capital")
                populasi = self._safe_extract_text(div, "span.country-population")
                luas = self._safe_extract_text(div, "span.country-area")

                countries.append({
                    "negara": negara,
                    "ibukota": ibukota,
                    "populasi": populasi,
                    "luas_km2": luas
                })

            df = pd.DataFrame(countries)
            self._save_to_csv(df, "countries.csv")
            return df
        except Exception as e:
            logging.error(f"Failed to scrape countries: {e}")
            return pd.DataFrame()

    def scrape_hockey(self, max_pages: int = 30) -> pd.DataFrame:
        """2. Scrapes hockey team data over multiple pages (pagination forms)."""
        url = f"{self.BASE_URL}/pages/forms/"
        logging.info("Starting scrape: Hockey Teams")
        
        all_teams = []
        for page in range(1, max_pages + 1):
            logging.info(f"Processing hockey teams page {page}/{max_pages}...")
            try:
                soup = self._get_soup(url, params={"page_num": page})
                rows = soup.select("tr.team")

                if not rows:
                    logging.info(f"No teams found on page {page}. Stopping pagination.")
                    break

                for row in rows:
                    team_name = self._safe_extract_text(row, "td.name")
                    year = self._safe_extract_text(row, "td.year")
                    wins = self._safe_extract_text(row, "td.wins")
                    losses = self._safe_extract_text(row, "td.losses")
                    ot_losses = self._safe_extract_text(row, "td.ot-losses")
                    pct = self._safe_extract_text(row, "td.pct")
                    gf = self._safe_extract_text(row, "td.gf")
                    ga = self._safe_extract_text(row, "td.ga")
                    diff = self._safe_extract_text(row, "td.diff")

                    all_teams.append({
                        "team_name": team_name,
                        "year": year,
                        "wins": wins,
                        "losses": losses,
                        "ot_losses": ot_losses,
                        "win_pct": pct,
                        "goals_for": gf,
                        "goals_against": ga,
                        "diff": diff
                    })
            except Exception as e:
                logging.error(f"Failed to scrape hockey teams on page {page}: {e}")
                break

        df = pd.DataFrame(all_teams)
        self._save_to_csv(df, "hockey_teams.csv")
        return df

    def scrape_oscars(self, start_year: int = 2010, end_year: int = 2015) -> pd.DataFrame:
        """3. Scrapes Oscar-winning films using AJAX requests."""
        url = f"{self.BASE_URL}/pages/ajax-javascript/"
        logging.info("Starting scrape: Oscar Winning Films (AJAX)")
        
        all_films = []
        for year in range(start_year, end_year + 1):
            logging.info(f"Processing Oscar films for year {year}...")
            try:
                films_data = self._get_json(url, params={"ajax": "true", "year": str(year)})
                
                for film in films_data:
                    all_films.append({
                        "tahun": year,
                        "judul": film.get("title", ""),
                        "nominasi": film.get("nominations", ""),
                        "menang_best_picture": "Ya" if film.get("best_picture") else "Tidak",
                        "poster_url": film.get("poster", "")
                    })
            except Exception as e:
                logging.error(f"Error scraping Oscar films for year {year}: {e}")
                continue

        df = pd.DataFrame(all_films)
        self._save_to_csv(df, "oscar_films.csv")
        return df

    def _save_to_csv(self, df: pd.DataFrame, filename: str):
        """Saves a DataFrame to CSV in the target directory."""
        if df.empty:
            logging.warning(f"DataFrame for {filename} is empty. Skipping save.")
            return
            
        os.makedirs(self.output_dir, exist_ok=True)
        filepath = os.path.join(self.output_dir, filename)
        df.to_csv(filepath, index=False)
        logging.info(f"Successfully saved {len(df)} records to: {filepath}")


def main():
    # Resolve the directory paths dynamically based on script location
    script_dir = os.path.dirname(os.path.abspath(__file__))
    workspace_dir = os.path.dirname(script_dir)
    output_dir = os.path.join(workspace_dir, "output", "mini-project")

    logging.info("=== Starting Mini Project Scraper ===")
    
    scraper = ScrapeThisSiteScraper(output_dir=output_dir, delay=2.0)

    # 1. Countries of the World
    scraper.scrape_countries()

    # 2. Hockey Teams (with forms, searching, pagination)
    scraper.scrape_hockey(max_pages=30)

    # 3. Oscar Winning Films (with AJAX and Javascript request)
    scraper.scrape_oscars(start_year=2010, end_year=2015)

    logging.info("=== Mini Project Scraper Completed ===")


if __name__ == "__main__":
    main()
