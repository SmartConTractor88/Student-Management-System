from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QApplication, QVBoxLayout, QLabel, QWidget, \
    QGridLayout, QLineEdit, QPushButton, QMainWindow, QTableWidget, \
    QTableWidgetItem, QDialog, QComboBox, QToolBar, QStatusBar

from PyQt6.QtGui import QAction, QIcon

import sys
import sqlite3

"""one class for each window of the App"""


class MainWindow(QMainWindow): 

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Student Management System")
        self.setMinimumSize(800, 600)

        file_menu = self.menuBar().addMenu("&File") # "&" a convention
        help_menu = self.menuBar().addMenu("&Help")
        edit_menu = self.menuBar().addMenu("&Edit")

        add_student_action = QAction(QIcon("icons/add.png"), "Add Student", self)
        add_student_action.triggered.connect(self.insert)
        file_menu.addAction(add_student_action)

        about_action = QAction("About", self)
        help_menu.addAction(about_action)
        about_action.setMenuRole(QAction.MenuRole.NoRole)

        search_action = QAction(QIcon("icons/search.png"), "Search", self)
        edit_menu.addAction(search_action)
        search_action.triggered.connect(self.search)

        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(("ID", "Name", "Course", 
                                              "Contact"))
        self.table.verticalHeader().setVisible(False) # hide the first index column 
        self.setCentralWidget(self.table) # specify the central widget

        # create a toolbar
        toolbar = QToolBar()
        toolbar.setMovable(True) # make the toolbar movable
        self.addToolBar(toolbar) # add toolbar to the window
        # add elements
        toolbar.addAction(add_student_action)
        toolbar.addAction(search_action)

        # create a status bar
        self.statusbar = QStatusBar()
        self.setStatusBar(self.statusbar)
        # add elements
        # detect a cell click
        self.table.cellClicked.connect(self.cell_clicked)

    def cell_clicked(self):
        edit_button = QPushButton("Edit Record")
        edit_button.clicked.connect(self.edit)

        delete_button = QPushButton("Delete Record")
        delete_button.clicked.connect(self.delete)

        # only add buttons if the status bar is empty
        buttons_exist = self.findChildren(QPushButton)
        if buttons_exist:
            for button in buttons_exist:
                self.statusbar.removeWidget(button)

        self.statusbar.addWidget(edit_button)
        self.statusbar.addWidget(delete_button)
    

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

    def search(self):
        dialog = SearchDialog()
        dialog.exec()

    def edit(self):
        dialog = EditDialog()
        dialog.exec()

    def delete(self):
        dialog = DeleteDialog()
        dialog.exec()


class EditDialog(QDialog): 
   
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Edit Record")
        self.setFixedWidth(300)
        self.setFixedHeight(400)

        # Student Name
        layout = QVBoxLayout()

        # Get student name
        index = main_window.table.currentRow()
        name = main_window.table.item(index, 1).text()

        # Get id from selected row
        self.student_id = main_window.table.item(index, 0).text()

        # Add student name widget
        self.student_name = QLineEdit(name)
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # Combo Box of Courses
        course_name = main_window.table.item(index, 2).text()
        self.course_name = QComboBox() # establish a selectbox widget
        courses = [" ","Business Administration","Computer Science",
                   "International Relations","Design/Marketing",
                   "Sports Management","Computer Engineering",
                   "Cybersecurity","Economics"]
        self.course_name.addItems(courses) # include the items of the list
        self.course_name.setCurrentText(course_name)
        layout.addWidget(self.course_name) # add widget to the layout

        # Type Phone Number
        phone_number = main_window.table.item(index, 3).text()
        self.phone_number = QLineEdit(phone_number)
        self.phone_number.setPlaceholderText("Phone number")
        layout.addWidget(self.phone_number)

        # Submit Button
        update = QPushButton("Update")
        update.clicked.connect(self.update_student)
        layout.addWidget(update)

        self.setLayout(layout) # apply the layout

    def update_student(self):

        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        cursor.execute("UPDATE students SET name = ?, course = ?, "
        "mobile = ? WHERE id = ?", 
        (self.student_name.text(), 
         self.course_name.itemText(self.course_name.currentIndex()), 
         self.phone_number.text(), 
         self.student_id))
        
        connection.commit()
        cursor.close()
        connection.close()
        # refresh the table
        main_window.load_data()

class DeleteDialog(QDialog):
    pass


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
        main_window.load_data()


class SearchDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Search Student")
        self.setFixedWidth(300)
        self.setFixedHeight(300)
    
        # create layout and input window
        layout = QVBoxLayout()
        self.student_name = QLineEdit()
        self.student_name.setPlaceholderText("Name")
        layout.addWidget(self.student_name)

        # search Button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search)
        layout.addWidget(search_button)

        self.setLayout(layout) # apply the layout

    def search(self):

        name = self.student_name.text()
        # Connect to the Database
        connection = sqlite3.connect("database.db")
        cursor = connection.cursor()
        result = cursor.execute("SELECT * FROM students WHERE name = ?", (name, ))

        row = list(result)
        print(row)
        items = main_window.table.findItems(name, Qt.MatchFlag.MatchFixedString)

        for item in items:
            main_window.table.item(item.row(), 1).setSelected(True)
            # row index must be 1 to access the location of student names

        cursor.close()
        connection.close()


app = QApplication(sys.argv)
main_window = MainWindow() # create main window
main_window.load_data()
main_window.show()
sys.exit(app.exec())

#class_init = MainWindow()