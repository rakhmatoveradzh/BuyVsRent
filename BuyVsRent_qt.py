#!/Users/eradzhrakhmatov/pyqtenv/bin/ python3


"""Command to translate .ui to .py file: pyuic5  window.ui >window.py """

import sys

from PySide6 import QtWidgets
from PySide6.QtWidgets import QMainWindow

import window

class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = window.Ui_Form()

        self.ui.setupUi(self)
        self.editUI()
        # self.get_values()
        self.ui.result_label.adjustSize()

        self.button_clicked()
        # self.initUI()

    def editUI(self):
        self.ui.estimate_button.clicked.connect(self.button_clicked)
        
    def get_values(self):
        self.property=int(self.ui.property_lineEdit.text())
        self.downpayment=int(self.ui.downpayment_spinbox.text()[:-1])/100
        self.interest=float(self.ui.interest_doubleSpinBox.text()[:-1])/100
        self.amortization=int(self.ui.amortization_lineEdit.text().split(' ')[0])
        self.property_tax=float(self.ui.property_tax_doubleSpinBox.text()[:-1])/100
        self.insurance=float(self.ui.insurance_doubleSpinBox.text()[:-1])/100
        self.maintenance=float(self.ui.maintenance_doubleSpinBox.text()[:-1])/100
        self.property_growth=float(self.ui.property_growth_doubleSpinBox.text()[:-1])/100
        self.rent=int(self.ui.rent_lineEdit.text())
        self.rent_increase=float(self.ui.rent_increase_doubleSpinBox.text()[:-1])/100
        self.investment=float(self.ui.investment_doubleSpinBox.text()[:-1])/100
        self.years=int(self.ui.years_lineEdit.text().split(' ')[0])

    def calculations(self):
        self.downpayment_value=self.property*self.downpayment
        self.loan_amount=self.property-self.downpayment_value
        monthly_interest=self.interest/12
        number_of_months=self.amortization*12

        '''Mortgage=P[i(1+i)^n/[(1+i)^n-1], P - load amount, i - monthly interest, n - total number of months'''
        self.mortgage=int(self.loan_amount*monthly_interest*((1+monthly_interest)**number_of_months)/((1+monthly_interest)**number_of_months-1))
        self.property_tax_cost=int(self.property*self.property_tax/12)
        self.insurance_cost=int(self.property*self.insurance/12)
        self.maintenance_cost=int(self.property*self.maintenance/12)
        self.total_payment=self.mortgage*self.amortization*12
        self.total_monthly=int(self.mortgage+self.property_tax_cost+self.insurance_cost+self.maintenance_cost)

        '''Appreciation=P(1+r/n)^nt, r - interest rate, n - number of times interest is applied in a year, n - number of years'''
        self.home_appreciation=int(self.property*(1+self.property_growth)**self.years)

        
        # self.mortgage_remaining=int(self.loan_amount*(1+self.interest)**self.years-self.mortgage*self.years*12)
        # self.investment_return=int(self.downpayment_value*(1+self.investment)**self.years)
        self.home_expenses=self.total_monthly*self.years*12

        '''calculate annual rent expenses considering rent increase and sum all and remaining mortgage amount'''
        self.mortgage_remaining=self.loan_amount
        self.investment_return=self.downpayment_value
        rent=self.rent*12
        year=1
        self.rent_expense=0
        while year <= self.years:
            # if year==1:
            #     rent=self.rent*12
            #     self.mortgage_remaining=self.loan_amount
            #     self.investment_return=self.downpayment_value
            #     year+=1
            #     continue
            self.mortgage_remaining=self.mortgage_remaining*(1+self.interest)-self.mortgage*12
            
            '''Investment return on downpayment and contribution equal to the 
            difference between monthly payments and rent price.
            if rent is less than mortgage plus other home expenses'''
            if self.rent<self.total_monthly:
                self.investment_return=(self.investment_return+(self.total_monthly-self.rent)*12)*(1+self.investment)

            if year==1:
                rent=self.rent*12
            else:    
                rent=rent+rent*self.rent_increase
            self.rent_expense+=rent
            year+=1

        if self.mortgage_remaining<0:
            self.mortgage_remaining=0

        self.home_profit=self.home_appreciation-self.mortgage_remaining
        self.investment_profit=int(self.investment_return)
        if self.home_profit>self.investment_profit:
            self.result=f"Buying home is better."
        else:
            self.result=f"Renting is better"

    def button_clicked(self):
        self.get_values()
        self.calculations()
        self.ui.result_label.adjustSize()
        self.ui.result_label.setText(f'Results: \nMortgage: {self.mortgage}\n'
        f'Property tax: {self.property_tax_cost}\n'
        f'Insurance cost: {self.insurance_cost}\n'
        f'Maintenance cost: {self.maintenance_cost}\n'

        f'Total mortgage payment: {self.total_payment}\n'
        f'Interest payment: {int(self.total_payment-self.loan_amount)}\n'
        f'Total monthly: {self.total_monthly}\n\n'
        f'In {self.years} years:\n'
        f'Home expenses: {self.home_expenses}\n'
        f'Mortgage remaining: {int(self.mortgage_remaining)}\n'
        f'Home appreciation: {self.home_appreciation}\n'
        f'Home profit: {int(self.home_profit)}\n'

        f'Investment return: {int(self.investment_return)}\n'
        f'Rent expenses: {int(self.rent_expense)}\n'
        f'Investment profit: {self.investment_profit}\n'
        f"{self.result}")

        # self.update()
    
    # def update(self):
    #     self.label.adjustSize()

    # def initUI(self):
    #     self.setGeometry(200, 200, 300, 300)
    #     self.setWindowTitle("Tech With Tim")

    #     self.label = QtWidgets.QLabel(self)
    #     self.label.setText("my first label!")
    #     self.label.move(50,50)

    #     self.b1 = QtWidgets.QPushButton(self)
    #     self.b1.setText("click me!")
    #     self.b1.clicked.connect(self.button_clicked)

def create_window():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow=MyWindow()
    MainWindow.editUI()
    MainWindow.show()
    sys.exit(app.exec_())
    


def main():
    create_window()
    # app = QApplication(sys.argv)
    # win = QMainWindow()
    # win.setGeometry(200,200,300,300) # sets the windows x, y, width, height
    # win.setWindowTitle("My first window!") # setting the window title
    # label = QLabel(win)
    # label.setText("my first label")
    # label.move(50, 50)  # x, y from top left hand corner.

    # b1 = QtWidgets.QPushButton(win)
    # b1.setText("click me")
    #b1.move(100,100) to move the button
    # win.show()
    # sys.exit(app.exec_())

if __name__ == '__main__':
    main()