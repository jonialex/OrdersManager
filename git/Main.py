from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QTableWidget

import sys
import mysql.connector
from database import databaseConnect

from Add_customer import Ui_Dialog_addCustomer
from Add_product import Ui_Dialog_addProduct
from Manage_order import Ui_Dialog_manageOrder

class Ui_MainWindow(object):

    def show_addCustomer(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_addCustomer()
        self.ui.setupUi(self.window)
        self.window.show()

        self.ui.Button_addCustomer.clicked.connect(self.getCustomer)
        
    
    def show_addProduct(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_addProduct()
        self.ui.setupUi(self.window)
        self.window.show()

        self.ui.Button_addProduct.clicked.connect(self.getProduct)
        self.ui.Button_addProduct.clicked.connect(self.getCategoryItems)

    def show_ManageOrder(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_manageOrder()
        self.ui.setupUi(self.window)
        self.window.show()

        self.ui.Button_newOrder.clicked.connect(self.getOrders)
    
    def getProduct(self):
        OrdersDB = databaseConnect()
        try:
            cursor = OrdersDB.cursor()
            
            #SQL query for getting the products from the database
            i = self.comboBox_category_3.currentIndex()
            sql = f"SELECT * FROM products WHERE category_id = {i+1}"
            cursor.execute(sql)
            result = cursor.fetchall()

            try:
                tablerow = 0
                for it in result:
                    
                    self.tableWidget_Catalog.setRowCount(len(result))
                    self.tableWidget_Catalog.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(it[1]))
                    self.tableWidget_Catalog.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(it[2])))
                    self.tableWidget_Catalog.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(it[3])))

                    
                    cursor.execute(f"SELECT * FROM categories WHERE category_id = {it[4]}")
                    res = cursor.fetchall()
                    self.tableWidget_Catalog.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(res[0][1])))
                    tablerow += 1

            except Exception as e:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText(f"Error code:\n{e}")
                msg.exec_()  # this will show our messagebox

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox

    
    def alterProduct(self):
        OrdersDB = databaseConnect()
        #TODO##########################################################################################################################
        with OrdersDB:
            cursor = OrdersDB.cursor()
            column_no = self.tableWidget_Catalog.currentColumn()

            column = ""
            if column_no == 0:
                column = "product_name"
            elif column_no == 1:
                column = "product_price"
            elif column_no == 2:
                column = "product_quantity"

            try:
                row = self.tableWidget_Catalog.currentRow()
                cln = self.tableWidget_Catalog.currentColumn()
                new_item = self.tableWidget_Catalog.currentItem().text()
                print(row)
                print(cln)
                print(column)
                print(new_item)
                sql = f"UPDATE products SET {column} = {new_item} WHERE product_id = {row+1}"
                cursor.execute(sql)

                OrdersDB.commit()

            except Exception as e:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText(f"Error code:\n{e}")
                msg.exec_()  # this will show our messagebox
                

    def getCustomer(self):
        OrdersDB = databaseConnect()
        try:
            cursor = OrdersDB.cursor()
            
            #SQL query for getting the products from the database
            sql = "SELECT * FROM customers"
            cursor.execute(sql)
            result = cursor.fetchall()

            tablerow = 0

            for it in result:
                self.tableWidget_customers.setRowCount(len(result))
                self.tableWidget_customers.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(it[1]))
                self.tableWidget_customers.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(it[2]))
                self.tableWidget_customers.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(it[3]))
                self.tableWidget_customers.setItem(tablerow, 3, QtWidgets.QTableWidgetItem(str(it[4])))
                self.tableWidget_customers.setItem(tablerow, 4, QtWidgets.QTableWidgetItem(it[5]))
                self.tableWidget_customers.setItem(tablerow, 5, QtWidgets.QTableWidgetItem(it[6]))
                tablerow += 1

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox
    
    def getCategoryItems(self):
        OrdersDB = databaseConnect()

        try:
            cursor = OrdersDB.cursor()

            #SQL query for getting the products from the database
            sql = "SELECT * FROM categories"
            cursor.execute(sql)
            result = cursor.fetchall()

            self.comboBox_category_3.clear()

            for it in result:
                self.comboBox_category_3.addItem(it[1])

        except Exception as e:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText(f"Error code:\n{e}")
                msg.exec_()  # this will show our messagebox
    
    def getOrders(self):
        OrdersDB = databaseConnect()

        try:
            cursor = OrdersDB.cursor()

            #SQL query for getting the products from the database
            orders_sql = "SELECT * FROM orders"
            cursor.execute(orders_sql)
            orders = cursor.fetchall()

            try:
                self.listWidget_orders.clear()
                for it in orders:
                    order_id = it[0]
                    customer_id = it[1]

                    order_sql = f"SELECT order_name FROM orders WHERE order_id = {order_id}"
                    cursor.execute(order_sql)
                    order = cursor.fetchall()

                    customer_sql = f"SELECT customer_name FROM customers WHERE customer_id = {customer_id}"
                    cursor.execute(customer_sql)
                    customer = cursor.fetchall()

                    self.listWidget_orders.addItem(f"{customer[0][0]}, {order[0][0]}")

            
            except Exception as e:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText(f"Error code:\n{e}")
                msg.exec_()  # this will show our messagebox

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox
    
    def getOrderItems(self):
        OrdersDB = databaseConnect()

        try:
            cursor = OrdersDB.cursor()
            
            #SQL query for getting the products from the database
            id = self.listWidget_orders.currentRow()
            sql = f"SELECT * FROM order_details WHERE order_id = {id+1}"
            cursor.execute(sql)
            order = cursor.fetchall()

            try:
                totalPrice = 0
                tablerow = 0
                for it in order:
                    sql2 = f"SELECT * FROM products WHERE product_id = {it[2]}"
                    cursor.execute(sql2)
                    product = cursor.fetchall()
                    self.tableWidget_orderDetails.setRowCount(len(order))
                    self.tableWidget_orderDetails.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(product[0][1]))
                    self.tableWidget_orderDetails.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(it[3])))
                    self.tableWidget_orderDetails.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(product[0][2])))
                    totalPrice = totalPrice + it[3]*product[0][2]
                    tablerow += 1

                self.label_totalPrice_Main.setText(f"{totalPrice} €")

            except Exception as e:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText(f"Error code:\n{e}")
                msg.exec_()  # this will show our messagebox

        except Exception as e:
                msg = QtWidgets.QMessageBox()
                msg.setWindowTitle("Warning")
                msg.setText(f"Error code:\n{e}")
                msg.exec_()  # this will show our messagebox

    def updateQuery(self):
        self.getCustomer()
        self.getProduct()
        self.getCategoryItems()
        self.getOrders()

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(823, 623)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.tabWidget_manager = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget_manager.setGeometry(QtCore.QRect(10, 10, 801, 561))
        self.tabWidget_manager.setObjectName("tabWidget_manager")

        self.tab_orders = QtWidgets.QWidget()
        self.tab_orders.setObjectName("tab_orders")

        self.tableWidget_orderDetails = QtWidgets.QTableWidget(self.tab_orders)
        self.tableWidget_orderDetails.setGeometry(QtCore.QRect(190, 0, 421, 531))

        self.tableWidget_orderDetails.setObjectName("tableWidget_orderDetails")
        self.tableWidget_orderDetails.setColumnCount(3)
        self.tableWidget_orderDetails.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orderDetails.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orderDetails.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_orderDetails.setHorizontalHeaderItem(2, item)

        self.listWidget_orders = QtWidgets.QListWidget(self.tab_orders)
        self.listWidget_orders.setGeometry(QtCore.QRect(0, 0, 191, 531))
        self.listWidget_orders.setObjectName("listWidget_orders")
        self.listWidget_orders.itemDoubleClicked.connect(self.getOrderItems)

        self.label = QtWidgets.QLabel(self.tab_orders)
        self.label.setGeometry(QtCore.QRect(620, 10, 81, 21))
        self.label.setObjectName("label")

        self.label_totalPrice_Main = QtWidgets.QLabel(self.tab_orders)
        self.label_totalPrice_Main.setGeometry(QtCore.QRect(720, 10, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_totalPrice_Main.setFont(font)
        self.label_totalPrice_Main.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_totalPrice_Main.setText("")
        self.label_totalPrice_Main.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_totalPrice_Main.setObjectName("label_totalPrice_Main")

        self.tabWidget_manager.addTab(self.tab_orders, "")
        self.tab_customers = QtWidgets.QWidget()
        self.tab_customers.setObjectName("tab_customers")

        self.tableWidget_customers = QtWidgets.QTableWidget(self.tab_customers)
        self.tableWidget_customers.setGeometry(QtCore.QRect(0, 0, 791, 531))

        self.tableWidget_customers.setObjectName("tableWidget_customers")
        self.tableWidget_customers.setColumnCount(6)
        self.tableWidget_customers.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_customers.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_customers.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_customers.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_customers.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_customers.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_customers.setHorizontalHeaderItem(5, item)

        self.tabWidget_manager.addTab(self.tab_customers, "")
        self.tab_catalog = QtWidgets.QWidget()
        self.tab_catalog.setObjectName("tab_catalog")

        self.tableWidget_Catalog = QtWidgets.QTableWidget(self.tab_catalog)
        self.tableWidget_Catalog.setGeometry(QtCore.QRect(0, 30, 791, 501))

        self.tableWidget_Catalog.setObjectName("tableWidget_Catalog")
        self.tableWidget_Catalog.setColumnCount(4)
        self.tableWidget_Catalog.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Catalog.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Catalog.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Catalog.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_Catalog.setHorizontalHeaderItem(3, item)

        self.comboBox_category_3 = QtWidgets.QComboBox(self.tab_catalog)
        self.comboBox_category_3.setGeometry(QtCore.QRect(0, 10, 121, 20))
        self.comboBox_category_3.setObjectName("comboBox_category_3")
        self.comboBox_category_3.activated.connect(self.getProduct)

        self.tabWidget_manager.addTab(self.tab_catalog, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 823, 21))
        self.menubar.setObjectName("menubar")
        self.menuTools = QtWidgets.QMenu(self.menubar)
        self.menuTools.setObjectName("menuTools")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.actionAdd_customer = QtWidgets.QAction(MainWindow)
        self.actionAdd_customer.setObjectName("actionAdd_customer")
        self.actionAdd_customer.triggered.connect(lambda: self.show_addCustomer())

        self.actionAdd_product = QtWidgets.QAction(MainWindow)
        self.actionAdd_product.setObjectName("actionAdd_product")
        self.actionAdd_product.triggered.connect(lambda: self.show_addProduct())

        self.actionAdd_category = QtWidgets.QAction(MainWindow)
        self.actionAdd_category.setObjectName("actionAdd_category")
        
        self.actionAdd_order = QtWidgets.QAction(MainWindow)
        self.actionAdd_order.setObjectName("actionAdd_order")
        self.actionAdd_order.triggered.connect(lambda: self.show_ManageOrder())

        self.menuTools.addAction(self.actionAdd_customer)
        self.menuTools.addAction(self.actionAdd_product)
        self.menuTools.addAction(self.actionAdd_order)
        self.menubar.addAction(self.menuTools.menuAction())

        self.retranslateUi(MainWindow)
        self.tabWidget_manager.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.updateQuery()

    def retranslateUi(self, MainWindow):
        try:
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
            item = self.tableWidget_orderDetails.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Product"))
            item = self.tableWidget_orderDetails.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Quantity"))
            item = self.tableWidget_orderDetails.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Price"))
            self.label.setText(_translate("MainWindow", "Total price:"))
            self.tabWidget_manager.setTabText(self.tabWidget_manager.indexOf(self.tab_orders), _translate("MainWindow", "Orders"))
            item = self.tableWidget_customers.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Name"))
            item = self.tableWidget_customers.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Address"))
            item = self.tableWidget_customers.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "City"))
            item = self.tableWidget_customers.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Postal Code"))
            item = self.tableWidget_customers.horizontalHeaderItem(4)
            item.setText(_translate("MainWindow", "Country"))
            item = self.tableWidget_customers.horizontalHeaderItem(5)
            item.setText(_translate("MainWindow", "Email"))
            self.tabWidget_manager.setTabText(self.tabWidget_manager.indexOf(self.tab_customers), _translate("MainWindow", "Customers"))
            item = self.tableWidget_Catalog.horizontalHeaderItem(0)
            item.setText(_translate("MainWindow", "Name"))
            item = self.tableWidget_Catalog.horizontalHeaderItem(1)
            item.setText(_translate("MainWindow", "Price"))
            item = self.tableWidget_Catalog.horizontalHeaderItem(2)
            item.setText(_translate("MainWindow", "Quantity"))
            item = self.tableWidget_Catalog.horizontalHeaderItem(3)
            item.setText(_translate("MainWindow", "Category"))
            self.comboBox_category_3.setCurrentText(_translate("MainWindow", "Select Category"))
            self.tabWidget_manager.setTabText(self.tabWidget_manager.indexOf(self.tab_catalog), _translate("MainWindow", "Catalog"))
            self.menuTools.setTitle(_translate("MainWindow", "Tools"))
            self.actionAdd_customer.setText(_translate("MainWindow", "Add customer"))
            self.actionAdd_product.setText(_translate("MainWindow", "Add product"))
            self.actionAdd_category.setText(_translate("MainWindow", "Add category"))
            self.actionAdd_order.setText(_translate("MainWindow", "Add order"))
        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
