import os
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QHBoxLayout, QVBoxLayout, QMessageBox, QFileDialog
from openpyxl import Workbook
from datetime import datetime


class TaskTracker(QWidget):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Task Tracker')

        self.lbl_task_title = QLabel('Task Title:')
        self.le_task_title = QLineEdit()
        self.lbl_employer_name = QLabel('Employer Name:')
        self.le_employer_name = QLineEdit()
        self.lbl_amount_paid = QLabel('Amount Paid:')
        self.le_amount_paid = QLineEdit()
        self.btn_submit = QPushButton('Submit')
        self.btn_submit.clicked.connect(self.submit_task)
        self.btn_generate_invoice = QPushButton('Generate Invoice')
        self.btn_generate_invoice.clicked.connect(self.generate_invoice)

        hbox1 = QHBoxLayout()
        hbox1.addWidget(self.lbl_task_title)
        hbox1.addWidget(self.le_task_title)

        hbox2 = QHBoxLayout()
        hbox2.addWidget(self.lbl_employer_name)
        hbox2.addWidget(self.le_employer_name)

        hbox3 = QHBoxLayout()
        hbox3.addWidget(self.lbl_amount_paid)
        hbox3.addWidget(self.le_amount_paid)

        vbox = QVBoxLayout()
        vbox.addLayout(hbox1)
        vbox.addLayout(hbox2)
        vbox.addLayout(hbox3)
        vbox.addWidget(self.btn_submit)
        vbox.addWidget(self.btn_generate_invoice)

        self.setLayout(vbox)
        self.show()

    def submit_task(self):
        task_title = self.le_task_title.text()
        employer_name = self.le_employer_name.text()
        amount_paid = self.le_amount_paid.text()

        if not employer_name:
            QMessageBox.warning(self, 'Warning', 'Employer name cannot be empty.')
            return

        employer_folder_path = os.path.join(os.getcwd(), employer_name)

        if not os.path.exists(employer_folder_path):
            os.mkdir(employer_folder_path)
            os.mkdir(os.path.join(employer_folder_path, 'paid'))
            os.mkdir(os.path.join(employer_folder_path, 'not_paid'))

        not_paid_folder_path = os.path.join(employer_folder_path, 'not_paid')
        task_folder_path = os.path.join(not_paid_folder_path, task_title)

        if os.path.exists(task_folder_path):
            QMessageBox.warning(self, 'Warning', 'Task already exists.')
            return

        os.mkdir(task_folder_path)

        # Save task information to a text file
        task_info_file_path = os.path.join(task_folder_path, 'task_info.txt')
        with open(task_info_file_path, 'w') as f:
            f.write(f'{task_title}\n')
            f.write(f'{amount_paid}\n')
            f.write(f'{datetime.now().strftime("%Y-%m-%d")}\n')

        QMessageBox.information(self, 'Success', 'Task submitted successfully.')

    def generate_invoice(self):
        employer_name = self.le_employer_name.text()

        if not employer_name:
            QMessageBox.warning(self, 'Warning', 'Employer name cannot be empty.')
            return

        employer_folder_path = os.path.join(os.getcwd(), employer_name)
        not_paid_folder_path = os.path.join(employer_folder_path, 'not_paid')
        paid_folder_path = os.path.join(employer_folder_path, 'paid')

        if not os.path.exists(not_paid_folder_path):
            QMessageBox.warning(self, 'Warning', 'No tasks found.')
            return

        # Create 'paid' folder if it doesn't exist
        if not os.path.exists(paid_folder_path):
            os.mkdir(paid_folder_path)

        # Create invoice workbook
        invoice_wb = Workbook()
        invoice_sheet = invoice_wb.active
        invoice_sheet['A1'] = 'Task Title'
        invoice_sheet['B1'] = 'Amount Paid'
        invoice_sheet['C1'] = 'Date'

        # Read task_info.txt files and add them to invoice
        row_index = 2
        for task_name in os.listdir(not_paid_folder_path):
            task_folder_path = os.path.join(not_paid_folder_path, task_name)
            task_info_file_path = os.path.join(task_folder_path, 'task_info.txt')

            if os.path.exists(task_info_file_path):
                with open(task_info_file_path, 'r') as task_info_file:
                    task_info = task_info_file.readlines()
                    task_title = task_info[0].strip()
                    amount_paid = task_info[1].strip()
                    date = task_info[2].strip()

                    invoice_sheet[f'A{row_index}'] = task_title
                    invoice_sheet[f'B{row_index}'] = amount_paid
                    invoice_sheet[f'C{row_index}'] = date

                    row_index += 1

                # Move task folder to 'paid' folder
                task_paid_folder_path = os.path.join(paid_folder_path, task_name)
                os.rename(task_folder_path, task_paid_folder_path)

        # Save invoice file in the employer folder
        date_str = datetime.today().strftime('%Y-%m-%d')
        invoice_file_path = os.path.join(employer_folder_path, f'invoice_{date_str}.xlsx')
        invoice_wb.save(invoice_file_path)

        QMessageBox.information(self, 'Success', 'Invoice generated successfully.')


if __name__ == '__main__':
    app = QApplication([])
    task_tracker = TaskTracker()
    app.exec_()
