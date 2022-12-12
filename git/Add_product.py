from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import sys
from database import databaseConnect

class Ui_Dialog_addProduct(object):

    def addProduct(self):
        OrdersDB = databaseConnect()
        try:
            cursor = OrdersDB.cursor()
            
            #Adding the product to the database
            sql = "INSERT INTO products (product_name, product_price, product_quantity, category_id) VALUES (%s, %s, %s, %s)"

            i = self.comboBox_category.currentIndex()
            val = (''.join(self.input_productName.text()),
                    ''.join(self.input_productPrice.text()),
                        ''.join(self.input_productQty.text()),
                            f'{i+1}'
                    )
            cursor.execute(sql, val)
            
            OrdersDB.commit()   # required to make the changes, otherwise no changes are made to the table.

            # Clearing text inputs
            self.input_productName.clear()
            self.input_productPrice.clear()
            self.input_productQty.clear()

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox
    
    def addCategory(self):
        OrdersDB = databaseConnect()
        try:
            cursor = OrdersDB.cursor()

            cursor.execute("SELECT category_name FROM categories")
            result = cursor.fetchall()
            print(result)
            sql = "INSERT IGNORE INTO categories (category_name) VALUES (%s)"
            val = ''.join(self.input_category.text()),

            cursor.execute(sql, val)

            OrdersDB.commit()

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox
    
    def getCategoryItems(self):
        OrdersDB = databaseConnect()
        cursor = OrdersDB.cursor()

        #SQL query for getting the products from the database
        sql = "SELECT * FROM categories"
        cursor.execute(sql)
        result = cursor.fetchall()

        self.comboBox_category.clear()

        for it in result:
            self.comboBox_category.addItem(it[1])

    def setupUi(self, Dialog_addProduct):
        Dialog_addProduct.setObjectName("Dialog_addProduct")
        Dialog_addProduct.resize(341, 212)

        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog_addProduct)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 321, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.label_p_category = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_p_category.setObjectName("label_p_category")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_p_category)

        self.comboBox_category = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.comboBox_category.setObjectName("comboBox_category")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.comboBox_category)

        self.label_p_name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_p_name.setObjectName("label_p_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_p_name)

        self.input_productName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_productName.setText("")
        self.input_productName.setObjectName("input_productName")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_productName)

        self.label_p_price = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_p_price.setObjectName("label_p_price")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_p_price)

        self.input_productPrice = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_productPrice.setObjectName("input_productPrice")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_productPrice)

        self.label_p_qty = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_p_qty.setObjectName("label_p_qty")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_p_qty)

        self.input_productQty = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_productQty.setObjectName("input_productQty")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.input_productQty)

        self.verticalLayout.addLayout(self.formLayout)

        self.Button_addProduct = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_addProduct.setObjectName("Button_addProduct")
        self.verticalLayout.addWidget(self.Button_addProduct)
        self.Button_addProduct.clicked.connect(self.addProduct)

        self.line = QtWidgets.QFrame(self.verticalLayoutWidget)
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.verticalLayout.addWidget(self.line)

        self.label = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.input_category = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_category.setObjectName("input_category")
        self.horizontalLayout.addWidget(self.input_category)

        self.Button_addCategory = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_addCategory.setObjectName("Button_addCategory")
        self.horizontalLayout.addWidget(self.Button_addCategory)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.Button_addCategory.clicked.connect(self.addCategory)
        self.Button_addCategory.clicked.connect(self.getCategoryItems)

        self.retranslateUi(Dialog_addProduct)
        QtCore.QMetaObject.connectSlotsByName(Dialog_addProduct)

        self.getCategoryItems()

    def retranslateUi(self, Dialog_addProduct):
        _translate = QtCore.QCoreApplication.translate
        Dialog_addProduct.setWindowTitle(_translate("Dialog_addProduct", "Add product"))
        self.label_p_category.setText(_translate("Dialog_addProduct", "Category"))
        self.comboBox_category.setCurrentText(_translate("Dialog_addProduct", "test"))
        self.comboBox_category.setItemText(0, _translate("Dialog_addProduct", "test"))
        self.comboBox_category.setItemText(1, _translate("Dialog_addProduct", "test2"))
        self.label_p_name.setText(_translate("Dialog_addProduct", "Name"))
        self.label_p_price.setText(_translate("Dialog_addProduct", "Price"))
        self.label_p_qty.setText(_translate("Dialog_addProduct", "Quantity"))
        self.Button_addProduct.setText(_translate("Dialog_addProduct", "Add product"))
        self.label.setText(_translate("Dialog_addProduct", "Add category:"))
        self.Button_addCategory.setText(_translate("Dialog_addProduct", "Add"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_addProduct = QtWidgets.QDialog()
    ui = Ui_Dialog_addProduct()
    ui.setupUi(Dialog_addProduct)
    Dialog_addProduct.show()
    sys.exit(app.exec_())
