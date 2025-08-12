The Stockholm Rental Price Tracker is a Python-based web scraping and data analysis tool that monitors apartment rental listings in Stockholm.
It automatically collects rental data from Blocket, stores raw HTML snapshots for reproducibility, extracts relevant details (such as price, location, size, and posting date), and saves them to a local SQLite database.

The project supports:

    Automated scraping using Playwright to capture fully rendered pages.

    Raw data storage (HTML files) to ensure future re-parsing is possible without re-scraping.

    Data parsing & cleaning with BeautifulSoup.

    Exploratory analysis to track price trends and availability over time.

    Visualization of trends using Python plotting libraries.
