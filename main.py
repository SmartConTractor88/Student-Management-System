from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem

from PyQt6.QtGui import QAction

import sys
import sqlite3

"""one class for each window of the App"""

class MainWindow(QMainWindow): 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")

        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        add_student_action = QAction("Add Student", self)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", 
                                              "Contact"))
        self.table.verticalHeader().setVisible(False) # hide the first index column 
        self.setCentralWidget(self.table) # specify the central widget

    def load_data(self):
        connection = sqlite3.connect("database.db")
        result = connection.execute("SELECT * FROM students")

        """#whenever the program is loaded, the following data will not be 
        added on top of existing data"""
        self.table.setRowCount(0)

        for row_number, row_data in enumerate(result):
            self.table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                self.table.setItem(row_number, column_number, 
                                   QTableWidgetItem(str(data)))
        connection.close()

        #grid = QGridLayout()
        #self.setLayout(grid)


app = QApplication(sys.argv)
run_app = MainWindow() # create main window
run_app.load_data()
run_app.show()
sys.exit(app.exec())

#class_init = MainWindow()