import sys
import mysql.connector as ms
from PyQt5 import QtCore, QtGui, QtWidgets

def databaseConnect():
    # Connect to the database
    try:
        OrdersDB = ms.connect(
            host = "localhost",
            user = "Admin",
            password = "admin",
            database = "ordersdatabase"
        )

        return OrdersDB

    except ms.Error as e:
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Connection warning")
        msg.setText(f"Error code:\n{e}")
        msg.exec_()  # this will show our messagebox

def createTables():
    OrdersDB = databaseConnect()
    cursor = OrdersDB.cursor()

    try:

        categories_tb = "CREATE TABLE categories (category_id INT AUTO_INCREMENT PRIMARY KEY, category_name VARCHAR(50))"
        products_tb = "CREATE TABLE products (product_id int AUTO_INCREMENT PRIMARY KEY, product_name VARCHAR(50), product_price DOUBLE, product_quantity int, category_id int)"
        customers_tb = "CREATE TABLE customers (customer_id int AUTO_INCREMENT PRIMARY KEY, customer_name VARCHAR(50), customer_address VARCHAR(50), customer_city VARCHAR(30), customer_postalCode int, customer_country VARCHAR(30), customer_email VARCHAR(50))"
        order_details_tb = "CREATE TABLE order_details (orderDetails_id int PRIMARY KEY AUTO_INCREMENT, order_id int, FOREIGN KEY (order_id) REFERENCES orders(order_id), product_id int, FOREIGN KEY (product_id) REFERENCES products(product_id), quantity int)"
        orders_tb = "CREATE TABLE orders (order_id int PRIMARY KEY AUTO_INCREMENT, customer_id int, FOREIGN KEY (customer_id) REFERENCES customers(customer_id))"

        tables = categories_tb, products_tb, customers_tb, order_details_tb, orders_tb
        for it in tables:
            cursor.execute(it)
        
    except ms.Error as e:
        msg = QtWidgets.QMessageBox()
        msg.setWindowTitle("Warning")
        msg.setText(f"Error code:\n{e}")
        msg.exec_()  # this will show our messagebox

def clearTables():
    OrdersDB = databaseConnect()
    cursor = OrdersDB.cursor()

    with OrdersDB:
        tables = ("order_details", "orders", "products", "customers", "categories")
        for table in tables:
            cursor.execute(f"DELETE FROM {table}")
            OrdersDB.commit()
            resetAI = f"ALTER TABLE {table} AUTO_INCREMENT = 1"
            cursor.execute(resetAI)
            OrdersDB.commit()

def deleteTables(table):
    OrdersDB = databaseConnect()
    cursor = OrdersDB.cursor()
    
    with OrdersDB:
        cursor.execute(f"DROP TABLE {table}")
        OrdersDB.commit()