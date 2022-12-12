from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import sys
from database import databaseConnect

class Ui_Dialog_addOrder(object):

    def getCustomerItems(self):
        OrdersDB = databaseConnect()
        cursor = OrdersDB.cursor()

        #SQL query for getting the customer names from the database
        sql = "SELECT customer_name FROM customers"
        cursor.execute(sql)
        result = cursor.fetchall()

        self.comboBox_selectCustomer_order.clear()
        for it in result:
            self.comboBox_selectCustomer_order.addItem(str(it[0]))

    def addOrder(self):
        OrdersDB = databaseConnect()
        try:
            cursor = OrdersDB.cursor()
            
            #Adding the order to the database
            sql = "INSERT INTO orders (customer_id, order_name) VALUES (%s, %s)"

            i = self.comboBox_selectCustomer_order.currentIndex()
            val = (f'{i+1}',
                    ''.join(self.lineEdit_orderName.text()),
                    )
            cursor.execute(sql, val)
            
            OrdersDB.commit()   # required to make the changes, otherwise no changes are made to the table.

            # Clearing text inputs
            self.lineEdit_orderName.clear()

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox

    def setupUi(self, Dialog_addOrder):

        Dialog_addOrder.setObjectName("Dialog_addOrder")
        Dialog_addOrder.resize(281, 142)

        self.comboBox_selectCustomer_order = QtWidgets.QComboBox(Dialog_addOrder)
        self.comboBox_selectCustomer_order.setGeometry(QtCore.QRect(10, 30, 261, 22))
        self.comboBox_selectCustomer_order.setObjectName("comboBox_selectCustomer_order")

        self.label = QtWidgets.QLabel(Dialog_addOrder)
        self.label.setGeometry(QtCore.QRect(10, 10, 261, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(Dialog_addOrder)
        self.label_2.setGeometry(QtCore.QRect(10, 60, 261, 16))
        self.label_2.setObjectName("label_2")

        self.lineEdit_orderName = QtWidgets.QLineEdit(Dialog_addOrder)
        self.lineEdit_orderName.setGeometry(QtCore.QRect(10, 80, 261, 20))
        self.lineEdit_orderName.setObjectName("lineEdit_orderName")

        self.pushButton_addOrder = QtWidgets.QPushButton(Dialog_addOrder)
        self.pushButton_addOrder.setGeometry(QtCore.QRect(10, 110, 261, 23))
        self.pushButton_addOrder.setObjectName("pushButton_addOrder")
        self.pushButton_addOrder.clicked.connect(self.addOrder)

        self.retranslateUi(Dialog_addOrder)
        QtCore.QMetaObject.connectSlotsByName(Dialog_addOrder)

        self.getCustomerItems()

    def retranslateUi(self, Dialog_addOrder):
        _translate = QtCore.QCoreApplication.translate
        Dialog_addOrder.setWindowTitle(_translate("Dialog_addOrder", "Add order"))
        self.label.setText(_translate("Dialog_addOrder", "Select customer"))
        self.label_2.setText(_translate("Dialog_addOrder", "Name the order"))
        self.pushButton_addOrder.setText(_translate("Dialog_addOrder", "Add order"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_addOrder = QtWidgets.QDialog()
    ui = Ui_Dialog_addOrder()
    ui.setupUi(Dialog_addOrder)
    Dialog_addOrder.show()
    sys.exit(app.exec_())
