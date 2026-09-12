from flask import Flask, request, render_template_string, redirect, url_for
import sqlite3

app = Flask(__name__)

# Base templates
BASE_TEMPLATE_WITH_NAV = """
<!DOCTYPE html>
<html>
<head>
    <title>My Shop</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 0; padding: 0; }
        header { background: #333; color: #fff; padding: 10px; text-align: center; }
        nav { background: #444; padding: 10px; text-align: center; }
        nav a { color: #fff; margin: 0 10px; text-decoration: none; font-weight: bold; }
        nav a:hover { text-decoration: underline; }
        .container { padding: 20px; }
        h1, h2 { color: #333; }
        ul { list-style: none; padding: 0; }
        li { background: #fff; margin: 5px 0; padding: 10px; border-radius: 5px;
             box-shadow: 0 1px 3px rgba(0,0,0,0.1); }
        .btn { background: #333; color: #fff; padding: 8px 12px; border-radius: 4px; text-decoration: none; }
        .btn:hover { background: #555; }
        footer { background: #333; color: #fff; text-align: center; padding: 10px; margin-top: 20px; }
    </style>
</head>
<body>
    <header><h1>🛒 My Shop</h1></header>
    <nav>
        <a href="{{ url_for('dashboard') }}">Dashboard</a>
        <a href="{{ url_for('products', category='All') }}">Products</a>
        <a href="{{ url_for('orders', username='wiener') }}">Orders</a>
        <a href="{{ url_for('wishlist', username='wiener') }}">Wishlist</a>
        <a href="{{ url_for('reviews', product='Laptop') }}">Reviews</a>
        <a href="{{ url_for('login') }}">Logout</a>
    </nav>
    <div class="container">{{ content|safe }}</div>
    <footer><p>&copy; 2025 My Shop</p></footer>
</body>
</html>
"""

BASE_TEMPLATE_NO_NAV = """
<!DOCTYPE html>
<html>
<head>
    <title>My Shop Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #f4f4f9; margin: 0; padding: 0; }
        header { background: #333; color: #fff; padding: 10px; text-align: center; }
        .container { padding: 20px; text-align: center; }
        h1, h2 { color: #333; }
        .grid { display: flex; justify-content: center; flex-wrap: wrap; gap: 20px; }
        .card-link { display: inline-block; width: 160px; text-decoration: none; color: inherit; }
        .card { width: 100%; padding: 20px; background: #fff; border-radius: 8px;
                box-shadow: 0 2px 5px rgba(0,0,0,0.1); text-align: center; transition: transform 0.05s ease-in-out; }
        .card:hover { transform: translateY(-2px); }
        .icon { font-size: 42px; margin-bottom: 8px; display: block; }
        .label { font-weight: bold; }
        footer { background: #333; color: #fff; text-align: center; padding: 10px; margin-top: 20px; }
    </style>
</head>
<body>
    <header><h1>🛒 My Shop</h1></header>
    <div class="container">{{ content|safe }}</div>
    <footer><p>&copy; 2025 My Shop</p></footer>
</body>
</html>
"""

def render_page(content, nav=True):
    if nav:
        return render_template_string(BASE_TEMPLATE_WITH_NAV, content=content)
    else:
        return render_template_string(BASE_TEMPLATE_NO_NAV, content=content)

# Dashboard (no nav bar, icons wrap the entire card as links)
@app.route('/dashboard')
def dashboard():
    content = f"""
    <h2>Dashboard</h2>
    <div class="grid">
        <a class="card-link" href="{url_for('products', category='All')}">
            <div class="card">
                <span class="icon">📦</span>
                <span class="label">Products</span>
            </div>
        </a>
        <a class="card-link" href="{url_for('orders', username='wiener')}">
            <div class="card">
                <span class="icon">🧾</span>
                <span class="label">Orders</span>
            </div>
        </a>
        <a class="card-link" href="{url_for('wishlist', username='wiener')}">
            <div class="card">
                <span class="icon">💖</span>
                <span class="label">Wishlist</span>
            </div>
        </a>
        <a class="card-link" href="{url_for('reviews', product='Laptop')}">
            <div class="card">
                <span class="icon">⭐</span>
                <span class="label">Reviews</span>
            </div>
        </a>
    </div>
    """
    return render_page(content, nav=False)

# Products
@app.route('/products')
def products():
    category = request.args.get('category', '')
    column = 'name'

    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    cursor.execute("SELECT DISTINCT category FROM products WHERE released = 1")
    categories = [row[0] for row in cursor.fetchall()]

    if category == "All":
        query = f"SELECT {column} FROM products WHERE released = 1"
    else:
        query = f"SELECT {column} FROM products WHERE category = '{category}' AND released = 1"

    try:
        cursor.execute(query)
        products = cursor.fetchall()
    except Exception as e:
        products = [(f"SQL Error: {e}",)]
    conn.close()

    content = f"""
    <h2>Products - {category}</h2>
    <nav>
        <strong>Categories:</strong>
        <a href="{url_for('products', category='All')}">All</a>
        {"".join([f"| <a href='{url_for('products', category=cat)}'>{cat}</a>" for cat in categories])}
    </nav>
    <ul>
        {''.join([f"<li>{p[0]}</li>" for p in products])}
    </ul>
    """
    return render_page(content, nav=True)

# Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = sqlite3.connect('shop.db')
        cursor = conn.cursor()
        query = f"SELECT username, password FROM users WHERE username = '{username}' AND password = '{password}'"
        try:
            cursor.execute(query)
            results = cursor.fetchall()
        except Exception as e:
            message = f"SQL Error: {e}"
            results = []
        conn.close()

        if results:
            return redirect(url_for('dashboard'))
        else:
            message = "Login failed or no data returned."

    content = f"""
    <h2>Login</h2>
    <form method="post">
        Username: <input name="username"><br>
        Password: <input name="password"><br>
        <input type="submit" value="Login" class="btn">
    </form>
    <p>{message}</p>
    """
    return render_page(content, nav=True)

# Orders
@app.route('/orders')
def orders():
    username = request.args.get('username', '')
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    query = f"SELECT product FROM orders WHERE username = '{username}'"
    try:
        cursor.execute(query)
        orders = cursor.fetchall()
    except Exception as e:
        orders = [(f"SQL Error: {e}",)]
    conn.close()

    content = "<h2>Order History</h2><ul>" + "".join([f"<li>{o[0]}</li>" for o in orders]) + "</ul>"
    return render_page(content, nav=True)

# Wishlist
@app.route('/wishlist')
def wishlist():
    username = request.args.get('username', '')
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    query = f"SELECT product FROM wishlist WHERE username = '{username}'"
    try:
        cursor.execute(query)
        wishlist = cursor.fetchall()
    except Exception as e:
        wishlist = [(f"SQL Error: {e}",)]
    conn.close()

    content = "<h2>Wishlist</h2><ul>" + "".join([f"<li>{w[0]}</li>" for w in wishlist]) + "</ul>"
    return render_page(content, nav=True)

# Reviews
@app.route('/reviews')
def reviews():
    product = request.args.get('product', '')
    conn = sqlite3.connect('shop.db')
    cursor = conn.cursor()
    query = f"SELECT review FROM reviews WHERE product = '{product}'"
    try:
        cursor.execute(query)
        reviews = cursor.fetchall()
    except Exception as e:
        reviews = [(f"SQL Error: {e}",)]
    conn.close()

    content = f"<h2>Reviews for {product}</h2><ul>" + "".join([f"<li>{r[0]}</li>" for r in reviews]) + "</ul>"
    return render_page(content, nav=True)

if __name__ == '__main__':
    app.run(debug=True)
