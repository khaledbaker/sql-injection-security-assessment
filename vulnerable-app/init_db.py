import sqlite3

conn = sqlite3.connect('shop.db')
cursor = conn.cursor()

# Drop old tables for clean setup
cursor.execute("DROP TABLE IF EXISTS products")
cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS orders")
cursor.execute("DROP TABLE IF EXISTS wishlist")
cursor.execute("DROP TABLE IF EXISTS reviews")

# Products table
cursor.execute('''
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    category TEXT NOT NULL,
    released INTEGER NOT NULL
)
''')

# Users table
cursor.execute('''
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    useame TEXrnT NOT NULL,
    password TEXT NOT NULL
)
''')

# Orders table
cursor.execute('''
CREATE TABLE orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    product TEXT NOT NULL
)
''')

# Wishlist table
cursor.execute('''
CREATE TABLE wishlist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    product TEXT NOT NULL
)
''')

# Reviews table
cursor.execute('''
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product TEXT NOT NULL,
    review TEXT NOT NULL
)
''')

# Insert mock products
products = [
    # Gifts
    ('Teddy Bear', 'Gifts', 1),
    ('Drone', 'Gifts', 0),
    ('Perfume', 'Gifts', 1),
    # Fashion
    ('Sneakers', 'Fashion', 1),
    ('Prototype Watch', 'Fashion', 0),
    ('Leather Jacket', 'Fashion', 1),
    # Electronics
    ('Smartphone', 'Electronics', 1),
    ('VR Headset', 'Electronics', 0),
    ('Laptop', 'Electronics', 1),
    # Books
    ('Python Guide', 'Books', 1),
    ('Unreleased Novel', 'Books', 0),
    ('SQL Injection Handbook', 'Books', 1)
]
cursor.executemany('INSERT INTO products (name, category, released) VALUES (?, ?, ?)', products)

# Insert sample users
users = [
    ('wiener', 'bluecheese'),
    ('administrator', 'supersecret')
]
cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', users)

# Insert sample orders
orders = [
    ('wiener', 'Teddy Bear'),
    ('wiener', 'Sneakers'),
    ('administrator', 'Laptop'),
    ('administrator', 'Perfume')
]
cursor.executemany('INSERT INTO orders (username, product) VALUES (?, ?)', orders)

# Insert sample wishlist
wishlist = [
    ('wiener', 'Drone'),
    ('wiener', 'Python Guide'),
    ('administrator', 'VR Headset'),
    ('administrator', 'Leather Jacket')
]
cursor.executemany('INSERT INTO wishlist (username, product) VALUES (?, ?)', wishlist)

# Insert sample reviews
reviews = [
    ('Teddy Bear', 'Great quality, my kid loves it!'),
    ('Sneakers', 'Comfortable and stylish.'),
    ('Laptop', 'Battery life is excellent.'),
    ('Python Guide', 'Very helpful for beginners.')
]
cursor.executemany('INSERT INTO reviews (product, review) VALUES (?, ?)', reviews)

conn.commit()
conn.close()
