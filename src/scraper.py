from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright, TimeoutError
import config
import random
import time


def getBlocketBostadPagination():

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        page.goto(config.blocketBostadURL)

        try:
            # Wait for any pagination link to appear (adjust selector as needed)
            page.wait_for_selector('a.qds-nyr6q5', timeout=10000)
        except TimeoutError:
            print("Pagination links not found within timeout!")
        html = page.content()
        browser.close()
# Now parse the rendered HTML with BeautifulSoup
    soup = BeautifulSoup(html, "html.parser")
    page_links = soup.find_all("a", href=True)
    print(page_links)
    page_numbers = []
    for link in page_links:
        href = link['href']
        if "page=" in href:
            text = link.get_text(strip=True)
            if text.isdigit():
                page_numbers.append(int(text))
    if page_numbers:
        last_page = max(page_numbers)
        print("Last page:", last_page)
        return last_page
    else:
        print("No page numbers found")


last_pagePagination = getBlocketBostadPagination()
listOfBlocketPages = []


def createBlocketURLs(ListOfBlocketURLs, lastBlocketPagePagination):
    blocketBostadURL2copy = config.blocketBostadURL2
    for pageNumber in range(1, last_pagePagination+1):
        pageURL = blocketBostadURL2copy.replace("1", str(pageNumber))
        listOfBlocketPages.append(pageURL)
        print(listOfBlocketPages[pageNumber-1])


createBlocketURLs(listOfBlocketPages, last_pagePagination)


def saveRawBlocketData(listOfBlocketPages):  # scrapes wrong data
    abs_path = "data/raw/blocket"
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        for index in range(0, last_pagePagination):
            pageNumber = index+1
            page = browser.new_page()
            page.goto(listOfBlocketPages[index])
            try:
                # Wait for any pagination link to appear (adjust selector as needed)
                # 20 second to make sure it loads
                page.wait_for_selector('a.qds-6d0zjo', timeout=20000)
            except TimeoutError:
                print(f"Scraping page: {pageNumber}...")
            html = page.content()
            # print(html)
            with open(f"{abs_path}/page"f"{pageNumber}.html", "w", encoding='utf8') as f:
                f.write(html)
                print(
                    f"Raw html data saved inside data/raw/blocket/page{pageNumber}.html")
            page.close()
            delay = random.uniform(1, 3)
            time.sleep(delay)
        browser.close()


saveRawBlocketData(listOfBlocketPages)
