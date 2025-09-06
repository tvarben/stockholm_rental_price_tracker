import sqlite3
import src.config
import textwrap

def count_listings(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM housing")
    return cursor.fetchone()[0]

# 2. Show first 5 listings


def show_sample_listings(conn, limit=5):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM housing LIMIT ?", (limit,))
    return cursor.fetchall()

# 3. Check for NULL values


def check_null_values(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        SUM(CASE WHEN location IS NULL THEN 1 ELSE 0 END) as null_locations,
        SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) as null_prices
    FROM housing
    """)
    return cursor.fetchone()


def avg_price_by_location(conn):
    """Get average prices with location normalization (SQLite compatible)"""
    cursor = conn.cursor()
    cursor.execute("""
    WITH cleaned_locations AS (
        SELECT 
            price,
            -- SQLite-compatible standardization
            CASE
                WHEN LOWER(location) LIKE '%stockholm%' THEN 'Stockholm'
                WHEN LOWER(location) LIKE '%bromma%' THEN 'Bromma'
                WHEN LOWER(location) LIKE '%spånga%' THEN 'Spånga'
                WHEN LOWER(location) LIKE '%enskede%' THEN 'Enskede'
                WHEN LOWER(location) LIKE '%kista%' THEN 'Kista'
                -- Fallback: Manual capitalization (simple version)
                ELSE UPPER(SUBSTR(TRIM(location), 1, 1)) || 
                     LOWER(SUBSTR(TRIM(location), 2))
            END as clean_location
        FROM housing
    )
    SELECT 
        clean_location as location,
        ROUND(AVG(price), 2) as avg_price,
        COUNT(*) as listings
    FROM cleaned_locations
    GROUP BY clean_location
    HAVING COUNT(*) >= 5  -- Only show locations with minimum 5 listings
    ORDER BY avg_price DESC
    """)

    results = cursor.fetchall()

    # Print formatted results
    print("\n{:<25} {:<15} {:<10}".format("Location", "Avg Price", "Listings"))
    print("-"*50)
    for row in results:
        print("{:<25} {:<15} {:<10}".format(row[0], f"SEK {row[1]:,}", row[2]))

    return results


def price_by_property_type_formatted(conn):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT 
        property_type,
        MIN(price) as min_price,
        ROUND(AVG(price), 2) as avg_price,
        MAX(price) as max_price,
        COUNT(*) as listings
    FROM housing
    GROUP BY property_type
    ORDER BY avg_price DESC
    """)
    results = cursor.fetchall()

    # Print formatted table
    print("\n{:<15} {:<15} {:<15} {:<15} {:<10}".format(
        "Property Type", "Min Price", "Avg Price", "Max Price", "Listings"
    ))
    print("-" * 70)
    for row in results:
        prop_type, min_price, avg_price, max_price, listings = row
        print("{:<15} {:<15} {:<15} {:<15} {:<10}".format(
            prop_type,
            f"SEK {min_price:,}",
            f"SEK {avg_price:,}",
            f"SEK {max_price:,}",
            listings
        ))

    return results


def most_expensive_listings_formatted(conn, limit=5):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT location, address, size_kvm, price, url
    FROM housing
    ORDER BY price DESC
    LIMIT ?
    """, (limit,))
    results = cursor.fetchall()

    print("\n{:<25} {:<25} {:<10} {:<15} {}".format(
        "Location", "Address", "Size (m²)", "Price", "URL"
    ))
    for i, row in enumerate(results, 1):
        location, address, size, price, url = row
        # Print full URL directly
        print("-" * 115)
        print("{:<25} {:<25} {:<10} {:<15} {}".format(
            textwrap.shorten(location, width=24, placeholder='...'),
            textwrap.shorten(address, width=24, placeholder='...'),
            size,
            f"SEK {price:,}",
            url  # Full URL here
        ))

    return results


def best_value_listings_formatted(conn, limit=5):
    cursor = conn.cursor()
    cursor.execute("""
    SELECT location, address, size_kvm, price, 
           (price*1.0/size_kvm) as price_per_sqm, url
    FROM housing
    WHERE size_kvm > 0
    ORDER BY price_per_sqm ASC
    LIMIT ?
    """, (limit,))
    results = cursor.fetchall()

    print("\n{:<25} {:<25} {:<10} {:<15} {:<15} {}".format(
        "Location", "Address", "Size (m²)", "Price", "Price/m²", "URL"
    ))
    for i, row in enumerate(results, 1):
        location, address, size, price, price_per_sqm, url = row
        # Print full URL directly
        print("-" * 130)
        print("{:<25} {:<25} {:<10} {:<15} {:<15.2f} {}".format(
            textwrap.shorten(location, width=24, placeholder='...'),
            textwrap.shorten(address, width=24, placeholder='...'),
            size,
            f"SEK {price:,}",
            price_per_sqm,
            url  # Full URL here
        ))

    return results


def run_test_queries(db_path):
    conn = sqlite3.connect(db_path)

    print("\n=== BASIC VERIFICATION ===")
    print("Total listings:", count_listings(conn))
    print("\nSample listings:", show_sample_listings(conn))
    print("\nNULL values (location, price):", check_null_values(conn))
    print("\n=== PRICE ANALYSIS ===")

    print("\nAverage price by location:")
    avg_price_by_location(conn)

    print("\nPrice by property type:")
    price_by_property_type_formatted(conn)

    print("\nMost expensive listings:")
    most_expensive_listings_formatted(conn)

    print("\nCheapest value listings:")
    best_value_listings_formatted(conn)

    conn.close()
