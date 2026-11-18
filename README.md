# Inventory and Sales Management for Small Business

A local academic project using Python Flask, MySQL, HTML, CSS and JavaScript.

## Features
- Dashboard: product count, stock count, low-stock count and total sales
- Product management: add, search, edit and delete products
- Sales: record transactions, validate available stock and automatically reduce inventory
- Reports: today's sales and product-wise stock/sales summary

## Setup (Windows)
1. Open this folder in VS Code.
2. Install dependencies:
   `python -m pip install -r requirements.txt`
   If Windows does not recognize `python`, use the full Python path, for example:
   `& "C:\\Users\\YOUR_USERNAME\\AppData\\Local\\Python\\pythoncore-3.14-64\\python.exe" -m pip install -r requirements.txt`
3. Copy `.env.example` to a new file named `.env`.
4. Put your own MySQL root password in `DB_PASSWORD` in `.env`. Do not share this file or password.
5. Your existing database should be named `inventory_sales` and have the `products` and `sales` tables. If needed, run `schema.sql` in MySQL.
6. Start the app with `python app.py` (or the full Python path as above).
7. Open http://127.0.0.1:5000 in your browser.

Check the database connection at http://127.0.0.1:5000/health.

## Notes
- Keep MySQL Server running while using the application.
- Dashboard values begin at zero until products and sales are added.
- Products with sales history cannot be deleted, preserving the sales report history.
- This is a local student prototype, not a production-ready system. Add authentication, access control, backups and deployment security before real business use.
