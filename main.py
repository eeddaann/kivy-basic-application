from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import mysql.connector as mdb
from kivy.properties import ObjectProperty
import sys


USER = 'cimlab'
PASS = 'CimLab'
DB = 'checkIt'
TABLE = 'GradesTable'

class InputForm(BoxLayout):
    'Input form entrty point'
    student_name = ObjectProperty()  # Variables fro KV file.
    course=ObjectProperty()
    grade = ObjectProperty()
    ip = ObjectProperty()

    def connect(self):
        'Creates database and table if not exists yet'
        con = mdb.connect(host=self.ip.text, user=USER, passwd=PASS)
        cur = con.cursor()
        cur.execute('CREATE DATABASE if not exists %s;'%DB)
        con.commit()  # Makes transaction
        con.close()  # Close transaction
        # Connects get the ip address from user
        con = mdb.connect(host=self.ip.text, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS %s \
                    (Id INTEGER(11) NOT NULL PRIMARY KEY AUTO_INCREMENT, \
                    StudentName varchar(8) NOT NULL,\
                    CourseName varchar(8) NOT NULL,\
                    Grade INTEGER(3) NOT NULL)"%TABLE)
        con.commit()
        con.close()

    def insert(self):
        'Inserts data to database'
        con = mdb.connect(host=self.ip.text, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()  # Making cursor
        if self.student_name.text.isalpha() and self.course.text.isalpha() and self.grade.text.isdigit():  # Check input
            cur.execute("INSERT INTO %s (StudentName,CourseName, Grade) VALUES ('%s','%s',%d)"
                        % (TABLE,self.student_name.text, self.course.text, int(self.grade.text)))  # Inserts user input to database
            con.commit()
            con.close()
        else:
            self.student_name.text = self.grade.text = 'Please enter valid data'  # Error msg for incorrect input.
            return
        self.student_name.text = self.grade.text = ''  # Clean text boxes
        self.student_name.focus = True  # Set focus on student name text box for another insertion.

    def displayRecords(self):
        'Display new form on screen'
        self.clear_widgets()  # Clears InputForm
        self.add_widget(ShowRecords(self.ip.text))  # Adds ShowRecords as new form

    def out(self):
        'Close application'
        sys.exit()


class ShowRecords(BoxLayout):
    'Shows the content of database'
    res = ObjectProperty()
    student_name = ObjectProperty()  # Variables fro KV file.
    course = ObjectProperty()
    grade = ObjectProperty()
    ip = ObjectProperty()

    def __init__(self, ip):
        'Builder of the class'
        super(ShowRecords, self).__init__()  # Call builder of BoxLayout because we don't use default builder
        con = mdb.connect(host=self.ip.text, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("SELECT * FROM %s"%TABLE)  # Quering database
        rows = cur.fetchall()  # Retrive all rows from query.
        self.show(rows)  # Call method to show results,

    def show(self, rows):
        'Shows results on screen'
        self.res.text = ''  # Clean previous results
        if not rows:
            self.res.text = 'No Records'  # Error msg
        else:
            for r in rows:
                    if len(r)>3:
                        self.res.text += r[1] +''+r[2]+''+str(r[3])+ '\n'
                    else:
                        self.res.text += r[0] + ' ' + str(r[1]) + '\n'  # Make readable msg
    def count_users(self):
        con = mdb.connect(host=self.ip.text, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("SELECT CourseName,COUNT(StudentName) FROM %s GROUP BY CourseName"%TABLE)
        rows=cur.fetchall()
        self.show(rows)

    def user_avg(self):
        con = mdb.connect(host=self.ip.text, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("select a CourseName, COUNT(StudentName) FROM %s group By CourseName"%TABLE)
        rows=cur.fetchall()
        self.show(rows)


    def good_students(self):
        con = mdb.connect(host=self.ip.text, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("SELECT StudentName, Grade FROM %s\
         WHERE grade=(SELECT MAX(Grade) FROM %s WHERE CourseName= 'Math')\
         AND CourseName='Math'"%TABLE)
        rows=cur.fetchall()
        self.show(rows)

    def display_input_data(self):
        self.clear_widgets()
        self.add_widget(InputForm())


    def out(self):
        'Close application'
        sys.exit()


class KivyApp(App):
    'Runs main loop uses kv file name kivy'
    pass


if __name__ == '__main__':  # Set entry point
    KivyApp().run()