from PyQt5 import QtCore, QtGui, QtWidgets
import mysql.connector
import sys
from database import databaseConnect

class Ui_Dialog_addCustomer(object):

    def addCustomer(self):
        OrdersDB = databaseConnect()
        try:
            cursor = OrdersDB.cursor()
            
            #Adding the customer to the database
            sql = "INSERT INTO customers (customer_name, customer_address, customer_city, customer_postalCode, customer_country, customer_email) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (''.join(self.input_customerName.text()),
                    ''.join(self.input_customerAddress.text()),
                        ''.join(self.input_customerCity.text()),
                            ''.join(self.input_customerPostalCode.text()),
                                ''.join(self.input_customerCountry.text()),
                                    ''.join(self.input_customerEmail.text()))
            cursor.execute(sql, val)

            OrdersDB.commit()   # required to make the changes, otherwise no changes are made to the table.

            # Clearing text inputs
            self.input_customerName.clear()
            self.input_customerAddress.clear()
            self.input_customerCity.clear()
            self.input_customerPostalCode.clear()
            self.input_customerCountry.clear()
            self.input_customerEmail.clear()

        except Exception as e:
            msg = QtWidgets.QMessageBox()
            msg.setWindowTitle("Warning")
            msg.setText(f"Error code:\n{e}")
            msg.exec_()  # this will show our messagebox

    def setupUi(self, Dialog_addCustomer):
        Dialog_addCustomer.setObjectName("Dialog_addCustomer")
        Dialog_addCustomer.resize(341, 211)

        self.verticalLayoutWidget = QtWidgets.QWidget(Dialog_addCustomer)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(10, 10, 321, 191))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")

        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")

        self.formLayout_addCustomer = QtWidgets.QFormLayout()
        self.formLayout_addCustomer.setObjectName("formLayout_addCustomer")

        self.label_c_name = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_c_name.setObjectName("label_c_name")
        self.formLayout_addCustomer.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label_c_name)
        self.input_customerName = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_customerName.setObjectName("input_customerName")

        self.label_c_address = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_c_address.setObjectName("label_c_address")
        self.formLayout_addCustomer.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_c_address)
        self.input_customerAddress = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_customerAddress.setObjectName("input_customerAddress")
        self.formLayout_addCustomer.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.input_customerAddress)

        self.label_c_city = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_c_city.setObjectName("label_c_city")
        self.formLayout_addCustomer.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_c_city)
        self.input_customerCity = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_customerCity.setObjectName("input_customerCity")
        self.formLayout_addCustomer.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.input_customerCity)

        self.label_c_postalcode = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_c_postalcode.setObjectName("label_c_postalcode")
        self.formLayout_addCustomer.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.label_c_postalcode)
        self.input_customerPostalCode = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_customerPostalCode.setObjectName("input_customerPostalCode")
        self.formLayout_addCustomer.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.input_customerPostalCode)

        self.label_c_country = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_c_country.setObjectName("label_c_country")
        self.formLayout_addCustomer.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_c_country)
        self.input_customerCountry = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_customerCountry.setObjectName("input_customerCountry")
        self.formLayout_addCustomer.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.input_customerCountry)

        self.label_c_email = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.label_c_email.setObjectName("label_c_email")
        self.formLayout_addCustomer.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.label_c_email)
        self.input_customerEmail = QtWidgets.QLineEdit(self.verticalLayoutWidget)
        self.input_customerEmail.setObjectName("input_customerEmail")
        self.formLayout_addCustomer.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.input_customerEmail)

        self.formLayout_addCustomer.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.input_customerName)
        self.verticalLayout.addLayout(self.formLayout_addCustomer)

        self.Button_addCustomer = QtWidgets.QPushButton(self.verticalLayoutWidget)
        self.Button_addCustomer.setObjectName("Button_addCustomer")
        self.verticalLayout.addWidget(self.Button_addCustomer)
        self.Button_addCustomer.clicked.connect(self.addCustomer)

        self.retranslateUi(Dialog_addCustomer)
        QtCore.QMetaObject.connectSlotsByName(Dialog_addCustomer)

    def retranslateUi(self, Dialog_addCustomer):
        _translate = QtCore.QCoreApplication.translate
        Dialog_addCustomer.setWindowTitle(_translate("Dialog_addCustomer", "Add customer"))
        self.label_c_name.setText(_translate("Dialog_addCustomer", "Name"))
        self.label_c_address.setText(_translate("Dialog_addCustomer", "Address"))
        self.label_c_city.setText(_translate("Dialog_addCustomer", "City"))
        self.label_c_postalcode.setText(_translate("Dialog_addCustomer", "Postal code"))
        self.label_c_country.setText(_translate("Dialog_addCustomer", "Country"))
        self.label_c_email.setText(_translate("Dialog_addCustomer", "Email"))
        self.Button_addCustomer.setText(_translate("Dialog_addCustomer", "Add customer"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog_addCustomer = QtWidgets.QDialog()
    ui = Ui_Dialog_addCustomer()
    ui.setupUi(Dialog_addCustomer)
    Dialog_addCustomer.show()
    sys.exit(app.exec_())
