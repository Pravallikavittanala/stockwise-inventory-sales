# StockWise – Inventory and Sales Management for Small Business

## 🌟 Project Overview

StockWise is a web-based Inventory and Sales Management System developed to help small businesses efficiently manage products, monitor stock levels, record sales transactions, and generate sales reports.

The application provides separate Admin and Staff accounts with role-based access control, ensuring that users can access only the features permitted to their roles.

StockWise is developed using Python Flask and MySQL and is deployed online using Railway.

## 🚀 Live Demo

**Live Website:** https://stockwise-inventory-sales-production.up.railway.app/

**GitHub Repository:** https://github.com/Pravallikavittanala/stockwise-inventory-sales

## ✨ Features

- **Admin and Staff Login:** Separate user accounts with secure password hashing.
- **Dashboard:** View inventory and sales information.
- **Product Management:** Add, edit, delete, and view product details.
- **Stock Management:** Monitor product quantities and low-stock levels.
- **Sales Management:** Record sales transactions.
- **Automatic Stock Deduction:** Product quantities are automatically updated after a sale.
- **User Management:** Admin can create and manage user accounts.
- **Sales Reports:** Admin can access sales reports.
- **Role-Based Access Control:** Restricts administrative features to authorized Admin users.
- **Business Registration:** Supports separate business accounts and business-specific data.

## 🛠️ Technologies Used

| Component | Technology |
|---|---|
| Frontend | HTML, CSS, JavaScript |
| Backend | Python, Flask |
| Database | MySQL |
| Authentication | Flask-Login |
| Password Security | Werkzeug |
| Database Connectivity | MySQL Connector |
| Configuration | Python Dotenv |
| Deployment | Railway |
| Version Control | Git and GitHub |

## 👥 User Roles

### Admin

- Manage products.
- Add and manage staff accounts.
- Record and view sales.
- Access sales reports.
- View inventory information.

### Staff

- View products.
- Record sales transactions.
- Access permitted application pages.
- Cannot access Admin-only reports or user management.

## 📂 Project Structure

```text
stockwise-inventory-sales/
│
├── app.py
├── main.py
├── database.py
├── schema.sql
├── requirements.txt
├── README.md
├── .gitignore
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
    ├── script.js
    └── ...
```

## ⚙️ Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/Pravallikavittanala/stockwise-inventory-sales.git
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

Add your local MySQL database configuration:

```env
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=inventory_sales
SECRET_KEY=your_secret_key
```

**Important:** Replace the example values with your own local database credentials. Never upload your `.env` file or expose database passwords and secret keys publicly.

### 5. Set Up the Database

- Create the MySQL database.
- Execute the SQL commands provided in `schema.sql`.
- Ensure that the database connection settings are configured correctly.

### 6. Run the Application

```bash
python app.py
```

Open the application in your browser:

```text
http://127.0.0.1:5000
```

## ☁️ Deployment

StockWise is deployed online using **Railway**.

- **Application Hosting:** Railway
- **Database Hosting:** Railway MySQL
- **Backend Server:** Gunicorn
- **Source Code Management:** GitHub

Access the deployed application:

https://stockwise-inventory-sales-production.up.railway.app/

## 🧪 Testing

The application has been functionally tested for:

- Admin and Staff login and logout.
- Role-based navigation.
- Restriction of Staff access to Admin-only reports.
- Product management operations.
- Sales recording.
- Automatic stock deduction after successful sales.
- Admin report access.
- Business registration and account creation.

## 🔮 Future Enhancements

- Graphical sales analytics and visual dashboards.
- Invoice generation.
- Supplier management.
- Export reports to PDF and Excel.
- Advanced inventory forecasting.
- Email notifications for low-stock products.

## 👩‍💻 Project Team

**Department:** Artificial Intelligence and Data Science  
**Institution:** CMR Institute of Technology  
**Project:** Semester V Mini-Project

- **Pravallika Vittanala** – 1CR24AD086
- **Nisarga Mary** – 1CR24AD075
- **Sindhu S** – 1CR24AD117

**Project Guide:** Prof. Bhavana

## 📜 License

This project is developed for academic purposes as a Semester V mini-project.

---

⭐ If you find this project useful, feel free to explore the repository and its features.
