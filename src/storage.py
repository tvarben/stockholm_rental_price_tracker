import sqlite3
import os
import json


def create_database(db_path):
    """Create database and table if they don't exist"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS housing")

    # Create housing table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS housing(
        id INTEGER PRIMARY KEY,
        location TEXT,
        address TEXT,
        property_type TEXT,
        size_kvm INTEGER,
        price INTEGER,
        available TEXT,
        until TEXT,
        url TEXT UNIQUE  -- Ensure no duplicate listings
    )
    """)
    connection.commit()
    connection.close()
    print(f"Database created/verified at {db_path}")


def load_json_to_db(db_path, processed_data_path):
    """Load processed JSON data into SQLite database"""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Prepare insert query
    insert_query = """
    INSERT OR IGNORE INTO housing (
        location, address, property_type, size_kvm,
        price, available, until, url
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    # Get all JSON files in processed data directory
    json_files = [
        f for f in os.listdir(processed_data_path)
        if f.endswith('.json')
    ]

    for json_file in json_files:
        file_path = os.path.join(processed_data_path, json_file)
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                listings = json.load(f)
                for listing in listings:
                    cursor.execute(insert_query, (
                        listing.get("location"),
                        listing.get("address"),
                        listing.get("property_type"),
                        listing.get("size_kvm"),
                        listing.get("price"),
                        listing.get("available"),
                        listing.get("until"),
                        listing.get("url")
                    ))
            print(f"Loaded data from {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

    connection.commit()
    connection.close()
    print("Data loading completed")
