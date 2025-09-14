from bs4 import BeautifulSoup
import re
import src.config
import json


def parse_html(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    results = []
    base_url = "https://bostad.blocket.se"  # Base URL to construct full links
    listings = soup.select('a[aria-label]')

    for listing in listings:
        aria_label = listing.get('aria-label', '')

        # Skip non-listing items (navigation links)
        if ' - ' not in aria_label:
            continue

        # Extract property type and location from aria-label
        property_type, _, location_str = aria_label.partition(' - ')

        # Extract listing URL
        relative_url = listing.get('href', '')
        listing_url = f"{base_url}{relative_url}" if relative_url else ""

        # Split location into address and area
        if ', ' in location_str:
            address, location = location_str.split(', ', 1)
        else:
            address = location_str
            location = location_str  # Fallback if no comma

        
        size_tag = listing.select_one('div.ea5jgjt0 p:last-child')
        size_text = size_tag.get_text(strip=True) if size_tag else ''
        size_match = re.search(r'(\d+)\s*m²?', size_text, re.IGNORECASE)
        size_kvm = int(size_match.group(1)) if size_match else None

        
        price_tag = listing.select_one('p.eq1ubw50')
        price_text = price_tag.get_text(strip=True) if price_tag else ''
        price_digits = ''.join(filter(str.isdigit, price_text))
        price = int(price_digits) if price_digits else None

        # Extract dates
        date_div = listing.select_one('div.e1ngqp210')
        if date_div:
            dates = [span.get_text(strip=True)
                     for span in date_div.select('span')]
            available = dates[0] if len(dates) > 0 else ''
            until = dates[1] if len(dates) > 1 else ''
        else:
            available, until = '', ''

        results.append({
            'location': location.strip(),
            'address': address.strip(),
            'property_type': property_type.strip(),
            'size_kvm': size_kvm,
            'price': price,
            'available': available.strip(),
            'until': until.strip(),
            'url': listing_url  
        })

    return results


def parse_and_save_data():
    for page in range(1, src.config.LAST_PAGE+1):
        raw_path = f"data/raw/blocket/page{page}.html"
        with open(raw_path, 'r') as f:
            html_content = f.read()
        parsed_data = parse_html(html_content)

        processed_path = f"data/processed/blocket/page{page}.json"
        with open(processed_path, "w", encoding="utf-8") as f:
            json.dump(parsed_data, f, ensure_ascii=False, indent=2)
        print(f"Saved processed data for {page} -> {processed_path}")
    return



