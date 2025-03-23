from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget

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
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", "Contact"))
        self.setCentralWidget(self.table) # specify the central widget

    def load_data(self):
        self.table
        pass

        #grid = QGridLayout()

        #self.setLayout(grid)

app = QApplication(sys.argv)
just_something = MainWindow()
just_something.show()
sys.exit(app.exec())

#class_init = MainWindow()