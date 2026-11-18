CREATE DATABASE IF NOT EXISTS inventory_sales;
USE inventory_sales;
CREATE TABLE IF NOT EXISTS products (
 product_id INT AUTO_INCREMENT PRIMARY KEY,
 product_name VARCHAR(100) NOT NULL,
 category VARCHAR(50),
 price DECIMAL(10,2) NOT NULL,
 quantity INT NOT NULL DEFAULT 0,
 low_stock_limit INT DEFAULT 5
);
CREATE TABLE IF NOT EXISTS sales (
 sale_id INT AUTO_INCREMENT PRIMARY KEY,
 product_id INT,
 quantity_sold INT NOT NULL,
 total_amount DECIMAL(10,2),
 sale_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
 FOREIGN KEY (product_id) REFERENCES products(product_id)
);
