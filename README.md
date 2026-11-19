# StockWise – Inventory and Sales Management for Small Business

## Project Overview

StockWise is a web-based Inventory and Sales Management System developed to help small businesses manage products, monitor stock levels, record sales transactions, and generate sales reports efficiently.

The application provides separate Admin and Staff accounts with role-based access control to ensure that users can access only the features permitted to their roles.

## Features

- **Admin and Staff Login:** Separate user accounts with secure password hashing.
- **Dashboard:** View inventory and sales information.
- **Product Management:** Add, edit, delete, and view product details.
- **Stock Management:** Monitor product quantities and low-stock levels.
- **Sales Management:** Record sales transactions.
- **Automatic Stock Deduction:** Update product quantities automatically after a sale.
- **User Management:** Admin can create and manage user accounts.
- **Sales Reports:** Admin can access sales reports.
- **Role-Based Access:** Restrict administrative features to Admin users.

## Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Authentication | Flask-Login |
| Password Security | Werkzeug |
| Database Connectivity | MySQL Connector |
| Configuration | Python Dotenv |

## User Roles

### Admin
- Manage products.
- Add and manage users.
- Record and view sales.
- Access sales reports.
- View inventory information.

### Staff
- View products.
- Record sales transactions.
- View permitted application pages.
- Cannot access Admin-only reports or user management.

## Project Structure

```text
inventory_sales_management/
│
├── app.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── setup_admin.html
│   ├── products.html
│   └── ...
│
└── static/
    ├── style.css
    └── script.js
```

## Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/stockwise-inventory-sales.git
```

### 2. Navigate to the Project Folder

```bash
cd stockwise-inventory-sales
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project directory.

Add your own database configuration:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=inventory_sales
SECRET_KEY=your_secret_key
```

Do not upload the `.env` file or expose database credentials publicly.

### 5. Set Up the Database

Create the MySQL database and execute the SQL commands provided in `schema.sql`.

### 6. Run the Application

```bash
python app.py
```

Open the following address in your browser:

```text
http://127.0.0.1:5000
```

## Testing

The application has been functionally tested for:

- Admin and Staff login and logout.
- Role-based navigation.
- Restriction of Staff access to Admin-only reports.
- Product management.
- Sales recording.
- Automatic stock deduction after successful sales.
- Admin report access.

## Future Enhancements

- Graphical sales analytics.
- Invoice generation.
- Supplier management.
- Export reports to PDF and Excel.
- Cloud deployment and online database integration.

## Project Team

**Department:** Artificial Intelligence and Data Science  
**Institution:** CMR Institute of Technology

- Pravallika Vittanala – 1CR24AD086
- Nisarga Mary – 1CR24AD075
- Sindhu S – 1CR24AD117

**Project Guide:** Prof. Bhavana

## License

This project is developed for academic purposes as a Semester V mini-project.