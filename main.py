from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QComboBox

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
        add_student_action.triggered.connect(self.insert)
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

        
    def insert(self):
        
        dialog = InsertDialog()
        dialog.exec()

class InsertDialog(QDialog): # create a dialog window

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Insert Student Data")
        self.setFixedWidth(300)
        self.setFixedHeight(300)

        # Student Name
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Combo Box of Courses
        self.course_name = QComboBox() # establish a selectbox widget
        courses = ["Business Administration","Computer Science",
                   "International Relations","Design/Marketing",
                   "Sports Management","Computer Engineering",
                   "Cybersecurity","Economics"]
        self.course_name.addItems(courses) # include the items of the list
        layout.addWidget(self.course_name) # add widget to the layout

        # Type Phone Number
        self.phone_number = QLineEdit()
        self.phone_number.setPlaceholderText("Phone number")
        layout.addWidget(self.phone_number)

        # Submit Button
        submit = QPushButton("Submit")
        submit.clicked.connect(self.add_student)
        layout.addWidget(submit)

        self.setLayout(layout) # apply the layout

    def add_student(self):
        
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        
        cursor.execute("SELECT MAX(id) FROM students")
        last_id = cursor.fetchone()[0]  # look for highest id

        # if no students exist, start from 1; otherwise, increment the last id
        if last_id is None:
            stud_id = 1
        else:
            stud_id = last_id + 1

        # format the new ID
        formatted_id = f"{stud_id:05d}"
        
        name = self.student_name.text()
        course = self.course_name.itemText(self.course_name.currentIndex())
        phone_number = self.phone_number.text()
        # Connect to the Database
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("INSERT INTO students VALUES (?,?,?,?)", 
                       (stud_id, name, course, phone_number))
        
        connection.commit() # Apply the query to the SQL database
        cursor.close()
        connection.close()
        run_app.load_data()
        

app = QApplication(sys.argv)
run_app = MainWindow() # create main window
run_app.load_data()
run_app.show()
sys.exit(app.exec())

#class_init = MainWindow()