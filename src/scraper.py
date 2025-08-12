import random
import time
import logging
from pathlib import Path
from typing import List, Optional
from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError, Browser, Page
import config

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scraper.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class BlocketBostadScraper:
    """A web scraper for Blocket Bostad property listings."""

    def __init__(self, base_url: str, output_dir: str = "data/raw/blocket"):
        self.base_url = base_url  # This should be blocketBostadURL2
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

        # Selectors - make them configurable
        # self.pagination_selector = 'a.qds-nyr6q5'
        # # Property listing links inside grid
        # self.content_selector = 'div.qds-6d0zjo.e6zz57q1 a[aria-label]'
        # REVERT IF NOT WORKING

        self.pagination_selector = 'a[class*="qds-nyr6q"]'
        self.content_selector = 'div[class*="qds-6d0zjo"] a[aria-label]'

        # Scraping settings
        self.timeout = 20000
        self.min_delay = 1
        self.max_delay = 3

    def _get_browser_page(self, browser: Browser) -> Page:
        """Create and configure a new browser page."""
        page = browser.new_page()
        # Add any page configuration here (user agent, viewport, etc.)
        return page

    def _wait_with_retry(self, page: Page, selector: str, max_retries: int = 2) -> bool:
        """Wait for selector with retry logic."""
        for attempt in range(max_retries + 1):
            try:
                page.wait_for_selector(selector, timeout=self.timeout)
                return True
            except TimeoutError:
                if attempt < max_retries:
                    logger.warning(f"Timeout waiting for {
                                   selector}, retrying... (attempt {attempt + 1})")
                    time.sleep(2)
                else:
                    logger.error(f"Failed to find {selector} after {
                                 max_retries + 1} attempts")
                    return False
        return False

    def get_last_page_number(self) -> Optional[int]:
        """Extract the last page number from pagination links."""
        logger.info("Getting pagination information...")

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = self._get_browser_page(browser)

            try:
                page.goto(self.base_url)

                if not self._wait_with_retry(page, self.pagination_selector):
                    return None

                html = page.content()
                soup = BeautifulSoup(html, "html.parser")

                page_numbers = self._extract_page_numbers(soup)

                if page_numbers:
                    last_page = max(page_numbers)
                    logger.info(f"Found {len(page_numbers)
                                         } pages, last page: {last_page}")
                    return last_page
                else:
                    logger.warning("No page numbers found")
                    return None

            except Exception as e:
                logger.error(f"Error getting pagination: {e}")
                return None
            finally:
                browser.close()

    def _extract_page_numbers(self, soup: BeautifulSoup) -> List[int]:
        """Extract page numbers from BeautifulSoup object."""
        page_numbers = []
        page_links = soup.find_all("a", href=True)

        for link in page_links:
            href = link.get('href', '')
            if "page=" in href:
                text = link.get_text(strip=True)
                if text.isdigit():
                    page_numbers.append(int(text))

        return page_numbers

    def generate_page_urls(self, last_page: int) -> List[str]:
        """Generate list of URLs for all pages to scrape."""
        logger.info(f"Generating URLs for {last_page} pages...")

        urls = []
        for page_num in range(1, last_page + 1):
            # Replace the page number in the base URL
            # Assumes the URL has page=1 that needs to be replaced with page=X
            url = self.base_url.replace("page=1", f"page={page_num}")
            urls.append(url)

        logger.info(f"Generated {len(urls)} URLs")
        return urls

    def scrape_page(self, browser: Browser, url: str, page_number: int) -> bool:
        """Scrape a single page and save the HTML."""
        logger.info(f"Scraping page {page_number}...")

        page = self._get_browser_page(browser)

        try:
            page.goto(url)

            # Wait for property listings to load
            if not self._wait_with_retry(page, self.content_selector):
                logger.warning(f"Property listings not found for page {
                               page_number}, continuing anyway...")
            else:
                # Count how many listings loaded
                listings_count = page.locator(self.content_selector).count()
                logger.info(
                    f"Found {listings_count} property listings on page {page_number}")

            html = page.content()

            # Save HTML to file
            file_path = self.output_dir / f"page{page_number}.html"
            with open(file_path, "w", encoding='utf8') as f:
                f.write(html)

            logger.info(f"Page {page_number} saved to {file_path}")
            return True

        except Exception as e:
            logger.error(f"Error scraping page {page_number}: {e}")
            return False
        finally:
            page.close()

    def scrape_all_pages(self, urls: List[str]) -> dict:
        """Scrape all pages with progress tracking."""
        logger.info(f"Starting to scrape {len(urls)} pages...")

        results = {
            'successful': 0,
            'failed': 0,
            'failed_pages': []
        }

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)

            try:
                for index, url in enumerate(urls):
                    page_number = index + 1

                    if self.scrape_page(browser, url, page_number):
                        results['successful'] += 1
                    else:
                        results['failed'] += 1
                        results['failed_pages'].append(page_number)

                    # Random delay between requests
                    if index < len(urls) - 1:  # Don't delay after last page
                        delay = random.uniform(self.min_delay, self.max_delay)
                        logger.debug(
                            f"Waiting {delay:.2f} seconds before next request...")
                        time.sleep(delay)

            finally:
                browser.close()

        logger.info(f"Scraping completed. Success: {
                    results['successful']}, Failed: {results['failed']}")
        if results['failed_pages']:
            logger.warning(f"Failed pages: {results['failed_pages']}")

        return results

    def run_full_scrape(self) -> dict:
        """Run the complete scraping process."""
        logger.info("Starting Blocket Bostad scraper...")

        # Get pagination info
        last_page = self.get_last_page_number()
        if not last_page:
            logger.error("Could not determine pagination, aborting...")
            return {'error': 'Pagination failed'}

        # Generate URLs
        urls = self.generate_page_urls(last_page)

        # Scrape all pages
        results = self.scrape_all_pages(urls)

        logger.info("Scraping process completed!")
        return results
