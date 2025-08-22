## Highlights
- Automated ETL pipeline for rental listings in Stockholm  
- Data scraped with Playwright and parsed with BeautifulSoup  
- Raw HTML snapshots stored for reproducibility  
- Structured data stored in SQLite for analysis  
- Results visualized in Jupyter Notebook (`results.ipynb`)  
- Dockerized for easy deployment  

## Overview
Stockholm Rental Price Tracker is a Python-based ETL pipeline that scrapes rental listings from Blocket Bostad, processes them, and stores the results in a local SQLite database for analysis.

The pipeline ensures reproducibility by saving raw HTML snapshots, then parsing and cleaning them into structured data. Finally, insights such as price distributions and cost-per-square-meter are visualized in Jupyter Notebook (results.ipynb).

For context, I have purposefully run the ETL pipeline once and uploaded the results in this repository to show what it looks like. Check  results.ipynb to see analysis. 

The project supports:

    Automated scraping using Playwright to capture fully rendered pages.

    Raw data storage (HTML files) to ensure future re-parsing is possible without re-scraping.

    Data parsing & cleaning with BeautifulSoup.

    Visualization of trends using Python plotting libraries and Jupyter Notebook.

What is an ETL pipeline?
An ETL pipeline is a system that extracts, transforms, and loads data from one or more sources into a destination, usually for analysis, reporting, or machine learning. The name ETL comes from the three main steps:
Extract (E): Collect data from different sources, such as databases, APIs, or files. 
Handles diverse formats like CSV, JSON, SQL tables, or web data.

Transform (T): Clean, enrich, or restructure the data.
Common tasks include removing duplicates, converting data types, aggregating values, and applying business rules.
Ensures the data is consistent and ready for analysis.

Load (L): Move the transformed data to a target storage system, such as a data warehouse, database, or cloud storage.
Ensures the data is accessible for reporting, dashboards, or analytics applications.

Blocket bostad ETL pipeline aims to get all rental listings from Blocket bostad Stockholm and do basic analysis on them such as diagrams, normal distribution and scatterplots

![plot1](https://github.com/user-attachments/assets/a9a787b9-aae6-4796-b675-22bb137c805a)
![plot2](https://github.com/user-attachments/assets/2bdb1548-dc85-4dcb-b7b3-44808615f988)
![plot3](https://github.com/user-attachments/assets/5bb61363-40cc-4572-891a-9e58c5c4c3ae)
![plot4](https://github.com/user-attachments/assets/17c87478-b100-4112-9d7a-b3cf970ed0c3)



To run this repo on linux: 

    git clone https://github.com/tvarben/stockholm_rental_price_tracker.git
    cd stockholm_rental_price_tracker/install
    chmod +x install_deps.sh
    ./install_deps.sh
    cd ..
    python -m src.main
    
Wait for scraping to complete...

The ETL process is complete, now it's time to visualize all listings from our database.
Open results.ipynb: 

    jupyter notebook

Click on Run and select Run All Cells.
Visualization of the rental listings should be visible.
    



It is also available as a Docker image on dockerhub: tvarben/blocket-bostad-etl-pipeline
But make sure to read the README.md in the container if new to docker because it differs to this one.

    docker pull tvarben/blocket-bostad-etl-pipeline
    docker run -it -p 8888:8888 tvarben/blocket-bostad-etl-pipeline
    cat README.md

