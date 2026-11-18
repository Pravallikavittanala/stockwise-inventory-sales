# StockWise – Inventory and Sales Management for Small Business

## Project Overview
StockWise is a web-based Inventory and Sales Management System developed using Python Flask and MySQL. It helps small businesses manage products, monitor stock levels, record sales transactions, and generate sales reports.

## Features

- **Dashboard:** Displays product count, available stock, low-stock count, and total sales.
- **Product Management:** Add, view, search, edit, and delete products.
- **Sales Management:** Record sales and automatically update product stock.
- **Reports:** View daily sales and product-wise stock and sales summaries.
- **User Authentication:** Secure login and logout functionality.
- **Role-Based Access:** Separate Admin and Staff permissions.
- **User Management:** Admin can create and manage staff accounts.

## User Roles

### Admin
- Access the dashboard.
- Manage products.
- Record and view sales.
- View reports.
- Add and manage staff users.

### Staff
- Access the dashboard.
- View products.
- Record sales.
- Cannot access admin-only reports or user management.

## Technologies Used

- Python
- Flask
- MySQL
- HTML
- CSS
- JavaScript
- Flask-Login
- Werkzeug Password Hashing

## Project Structure

```text
stockwise-inventory-sales/
│
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
├── .gitignore
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── login.html
│   ├── products.html
│   ├── product_form.html
│   ├── sales.html
│   ├── reports.html
│   ├── users.html
│   ├── user_form.html
│   └── setup_admin.html
│
└── static/
    ├── style.css
    └── script.js
```

## Installation and Setup

1. Clone this repository.
2. Install the required Python packages:

   ```bash
   pip install -r requirements.txt
   ```

3. Install and start MySQL Server.
4. Create the database and tables using `schema.sql`.
5. Configure your database connection details in a local `.env` file according to `database.py`.
6. Run the Flask application:

   ```bash
   python app.py
   ```

7. Open your browser and visit:

   `http://127.0.0.1:5000`

## Security

- Passwords are stored using password hashing.
- Login sessions are managed using Flask-Login.
- Access to admin features is restricted by user role.
- Database credentials must be stored in `.env`.
- Never upload `.env` or passwords to GitHub.

## Future Enhancements

- Online deployment.
- Inventory alerts and notifications.
- Advanced sales analytics.
- Export reports to PDF and Excel.

## Project Purpose

This project is developed as an academic mini-project to demonstrate inventory management, sales tracking, database connectivity, and web application development.

**Project Name:** Inventory and Sales Management for Small Business  
**Institute:** CMR Institute of Technology  
**Department:** Artificial Intelligence and Data Science
