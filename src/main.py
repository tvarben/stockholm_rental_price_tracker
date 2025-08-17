#!/usr/bin/env python3
"""
Main entry point for Blocket Bostad pipeline.
"""
import sqlite3
import logging
from src.scraper import BlocketBostadScraper
import src.config
import sys
import os
import src.parser
import src.storage
# Add parent directory to path to find config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Configure logging
logger = logging.getLogger(__name__)


def main():
    """Main function to run the scraper."""
    try:
        scraper = BlocketBostadScraper(
            base_url=src.config.blocketBostadURL2
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

    print("Initiazing intermediary process by saving parsed data. ")
    src.parser.parse_and_save_data()

    # we create database with create_database(src.config.DATABASE_NAME)
    print("creating database if not already exist")
    src.storage.create_database(src.config.DATABASE_NAME)
    # load json into database with create_database(src.config.DATABASE_NAME)
    src.storage.load_json_to_db(
        src.config.DATABASE_NAME, src.config.PROCESSED_DATA_PATH)

    connection = sqlite3.connect(src.config.DATABASE_NAME)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM housing")
    count = cursor.fetchone()[0]
    print(f"Total records in database: {count}")
    connection.close()


if __name__ == "__main__":
    main()
