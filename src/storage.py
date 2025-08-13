
import sqlite3
from . import config

# define connection and cursor

connection = sqlite3.connect(config.DATABASE_NAME)

cursor = connection.cursor()

# create stores table

command1 = """CREATE TABLE IF NOT EXISTS
housing(id INTEGER PRIMARY KEY, 
        location TEXT,
        address TEXT,
        property_type TEXT,
        size_kvm INTEGER,
        price INTEGER,
        available TEXT,
        until TEXT,
        link TEXT
        )"""

# TESTING SQL QUERIES
# cursor.execute(command1)
# cursor.execute(
#     "INSERT into housing VALUES (1, 'STOCKHOLM', 'MASKROSSTIGEN 3', 'HOUSE', 300, 10000000, 'NOW', '2027')")
# cursor.execute("SELECT * FROM housing")
# results1 = cursor.fetchall()
# print(results1)
# cursor.execute("SELECT property_type FROM housing", ())
# results = cursor.fetchall()
# print(results)
