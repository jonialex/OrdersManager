from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import sys

from Add_order import Ui_Dialog_addOrder
from database import databaseConnect


class Ui_Dialog_manageOrder(object):

    def show_addOrder(self):
        self.window = QtWidgets.QDialog()
        self.ui = Ui_Dialog_addOrder()
        self.ui.setupUi(self.window)
        self.window.show()

        self.ui.pushButton_addOrder.clicked.connect(self.getOrderItems)

    def getOrderItems(self):
        OrdersDB = databaseConnect()

        cursor = OrdersDB.cursor()

        #SQL query for getting the order names from the database
        sql = "SELECT * FROM orders"
        cursor.execute(sql)
        result = cursor.fetchall()

        self.comboBox_selectOrder.clear()
        for it in result:
            sql2 = f"SELECT customer_name FROM customers WHERE customer_id = {it[1]}"
            cursor.execute(sql2)
            result2 = cursor.fetchall()
            self.comboBox_selectOrder.addItem(f"{result2[0][0]}, {it[2]}")
        
    def getCategoryItems(self):
        OrdersDB = databaseConnect()
        cursor = OrdersDB.cursor()

        #SQL query for getting the categories from the database
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        result = cursor.fetchall()

        self.comboBox_selectCategory.clear()

        for it in result:
            self.comboBox_selectCategory.addItem(it[1])

    def getProductItems(self):
        OrdersDB = databaseConnect()
        cursor = OrdersDB.cursor()

        i = self.comboBox_selectCategory.currentIndex()
        #SQL query for getting the products from the database
        sql = f"SELECT * FROM products WHERE category_id = {i+1}"
        cursor.execute(sql)
        result = cursor.fetchall()

        self.comboBox_selectProduct.clear()

        for it in result:
            self.comboBox_selectProduct.addItem(it[1])
    
    def addProductToOrder(self):
        OrdersDB = databaseConnect()

        try:
            cursor = OrdersDB.cursor()

            #Adding the product to the order
            sql = "INSERT INTO order_details (order_id, product_id, quantity) VALUES (%s, %s, %s)"
            i = self.comboBox_selectOrder.currentIndex()

            p_name = self.comboBox_selectProduct.currentText()
            id_sql = f"SELECT product_id FROM products WHERE product_name = '{p_name}'"
            cursor.execute(id_sql)
            id = cursor.fetchall()

            val = (f'{i+1}',
                    f'{id[0][0]}',
                        ''.join(self.lineEdit_qtyProduct.text())
                    )
            cursor.execute(sql, val)

            OrdersDB.commit()

            self.lineEdit_qtyProduct.clear()

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox

    def getOrder(self):
        OrdersDB = databaseConnect()
        cursor = OrdersDB.cursor()
        
        #SQL query for getting the products from the database
        id = self.comboBox_selectOrder.currentIndex()
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
                self.tableWidget.setRowCount(len(order))
                self.tableWidget.setItem(tablerow, 0, QtWidgets.QTableWidgetItem(product[0][1]))
                self.tableWidget.setItem(tablerow, 1, QtWidgets.QTableWidgetItem(str(it[3])))
                self.tableWidget.setItem(tablerow, 2, QtWidgets.QTableWidgetItem(str(product[0][2])))
                totalPrice = totalPrice + it[3]*product[0][2]
                tablerow += 1

            self.label_totalPrice.setText(f"{totalPrice} €")

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox
        


    def updateQuery(self):
        self.getOrderItems()
        self.getCategoryItems()
        self.getProductItems()
        self.getOrder

    def setupUi(self, Dialog_manageOrder):

        Dialog_manageOrder.setObjectName("Dialog_manageOrder")
        Dialog_manageOrder.resize(560, 732)

        self.line = QtWidgets.QFrame(Dialog_manageOrder)
        self.line.setGeometry(QtCore.QRect(270, 10, 31, 711))
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")

        self.comboBox_selectCategory = QtWidgets.QComboBox(Dialog_manageOrder)
        self.comboBox_selectCategory.setGeometry(QtCore.QRect(10, 100, 261, 22))
        self.comboBox_selectCategory.setObjectName("comboBox_selectCategory")
        self.comboBox_selectCategory.activated.connect(self.getProductItems)


        self.comboBox_selectProduct = QtWidgets.QComboBox(Dialog_manageOrder)
        self.comboBox_selectProduct.setGeometry(QtCore.QRect(10, 150, 201, 22))
        self.comboBox_selectProduct.setObjectName("comboBox_selectProduct")

        self.lineEdit_qtyProduct = QtWidgets.QLineEdit(Dialog_manageOrder)
        self.lineEdit_qtyProduct.setGeometry(QtCore.QRect(220, 150, 31, 20))
        self.lineEdit_qtyProduct.setObjectName("lineEdit_qtyProduct")

        self.label_2 = QtWidgets.QLabel(Dialog_manageOrder)
        self.label_2.setGeometry(QtCore.QRect(10, 80, 261, 16))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(Dialog_manageOrder)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 201, 21))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(Dialog_manageOrder)
        self.label_4.setGeometry(QtCore.QRect(260, 150, 21, 21))
        self.label_4.setObjectName("label_4")

        self.Button_addToOrder = QtWidgets.QPushButton(Dialog_manageOrder)
        self.Button_addToOrder.setGeometry(QtCore.QRect(10, 180, 261, 23))
        self.Button_addToOrder.setObjectName("Button_addToOrder")
        self.Button_addToOrder.clicked.connect(self.addProductToOrder)
        self.Button_addToOrder.clicked.connect(self.getOrder)


        self.comboBox_selectOrder = QtWidgets.QComboBox(Dialog_manageOrder)
        self.comboBox_selectOrder.setGeometry(QtCore.QRect(10, 30, 211, 22))
        self.comboBox_selectOrder.setObjectName("comboBox_selectOrder")

        self.Button_newOrder = QtWidgets.QPushButton(Dialog_manageOrder)
        self.Button_newOrder.setGeometry(QtCore.QRect(230, 30, 41, 23))
        self.Button_newOrder.setObjectName("Button_newOrder")
        self.Button_newOrder.clicked.connect(lambda: self.show_addOrder())


        self.label_5 = QtWidgets.QLabel(Dialog_manageOrder)
        self.label_5.setGeometry(QtCore.QRect(10, 10, 211, 21))
        self.label_5.setObjectName("label_5")
        self.line_2 = QtWidgets.QFrame(Dialog_manageOrder)
        self.line_2.setGeometry(QtCore.QRect(10, 56, 261, 31))
        self.line_2.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.tableWidget = QtWidgets.QTableWidget(Dialog_manageOrder)
        self.tableWidget.setGeometry(QtCore.QRect(300, 20, 251, 671))

        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setRowCount(0)

        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        self.tableWidget.setColumnWidth(0, 100)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        self.tableWidget.setColumnWidth(1, 75)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        self.tableWidget.setColumnWidth(2, 75)

        self.label_totalPrice = QtWidgets.QLabel(Dialog_manageOrder)
        self.label_totalPrice.setGeometry(QtCore.QRect(426, 700, 121, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_totalPrice.setFont(font)
        self.label_totalPrice.setText("")
        self.label_totalPrice.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_totalPrice.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.label_totalPrice.setObjectName("label_totalPrice")
        self.label_6 = QtWidgets.QLabel(Dialog_manageOrder)
        self.label_6.setGeometry(QtCore.QRect(300, 700, 131, 21))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_6.setFont(font)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Dialog_manageOrder)
        QtCore.QMetaObject.connectSlotsByName(Dialog_manageOrder)

        self.updateQuery()

    def retranslateUi(self, Dialog_manageOrder):
        _translate = QtCore.QCoreApplication.translate
        Dialog_manageOrder.setWindowTitle(_translate("Dialog_manageOrder", "Manage order"))
        self.label_2.setText(_translate("Dialog_manageOrder", "Select category"))
        self.label_3.setText(_translate("Dialog_manageOrder", "Select product"))
        self.label_4.setText(_translate("Dialog_manageOrder", "pcs."))
        self.Button_addToOrder.setText(_translate("Dialog_manageOrder", "Add to order"))
        self.Button_newOrder.setText(_translate("Dialog_manageOrder", "New"))
        self.label_5.setText(_translate("Dialog_manageOrder", "Select order"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog_manageOrder", "Product"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog_manageOrder", "Quantity"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog_manageOrder", "Price"))
        self.label_6.setText(_translate("Dialog_manageOrder", "Total price:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_manageOrder = QtWidgets.QDialog()
    ui = Ui_Dialog_manageOrder()
    ui.setupUi(Dialog_manageOrder)
    Dialog_manageOrder.show()
    sys.exit(app.exec_())
