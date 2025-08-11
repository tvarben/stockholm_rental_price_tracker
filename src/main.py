#!/usr/bin/env python3
"""
Main entry point for Blocket Bostad scraper.
"""

import logging
from scraper import BlocketBostadScraper
import config
import sys
import os

# Add parent directory to path to find config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Configure logging
logger = logging.getLogger(__name__)


def main():
    """Main function to run the scraper."""
    try:
        scraper = BlocketBostadScraper(
            base_url=config.blocketBostadURL2
        )

        results = scraper.run_full_scrape()

        if 'error' not in results:
            print(f"\n✅ Scraping Summary:")
            print(f"   Successfully scraped: {results['successful']} pages")
            print(f"   Failed: {results['failed']} pages")
            if results['failed_pages']:
                print(f"   Failed page numbers: {results['failed_pages']}")
        else:
            print(f"❌ Scraping failed: {results['error']}")

    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")
        print(f"❌ Scraping failed with error: {e}")


if __name__ == "__main__":
    main()
