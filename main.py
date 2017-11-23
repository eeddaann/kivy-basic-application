from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
import mysql.connector as mdb
from kivy.properties import ObjectProperty
import sys

#credentials
USER = 'cimlab'
PASS = 'CimLab'
DB = 'checkIt'
TABLE = 'GradesTable'

class InputForm(BoxLayout):
    # Input form landing page
    student_name = ObjectProperty()  # Variables for KV file.
    course=ObjectProperty()
    grade = ObjectProperty()
    ip = ObjectProperty()

    def connect(self):
        # Create scheme if not exist and creates table if not exists
        con = mdb.connect(host=self.ip.text,port=3306, user=USER, passwd=PASS)
        cur = con.cursor()
        cur.execute('CREATE DATABASE if not exists %s;'%DB)
        con.commit()  # Makes transaction
        con.close()  # Close connection
        # Connection will get the host ip from the user
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
        # Insert data to table, Connection will get the host ip from the user
        con = mdb.connect(host=self.ip.text, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        # input validation
        if self.student_name.text.isalpha() and self.course.text.isalpha() and self.grade.text.isdigit():
            cur.execute("INSERT INTO %s (StudentName,CourseName, Grade) VALUES ('%s','%s',%d)"
                        % (TABLE,self.student_name.text, self.course.text, int(self.grade.text)))  # Insert user's input to DB
            con.commit()
            con.close()
        else:
            self.student_name.text = self.grade.text = 'Please enter valid data'  # Error msg for incorrect input.
            return
        self.student_name.text = self.grade.text = ''  # Clean text boxes
        self.student_name.focus = True  # Set focus on student name text box for another insertion.

    def display_records(self):
        # Display new form on screen
        self.clear_widgets()  # Clear InputForm
        self.add_widget(ShowRecords(self.ip.text))  # Add ShowRecords as a new form

    def out(self):
        # Close application
        sys.exit()


class ShowRecords(BoxLayout):
    # Show the records on the DB
    res = ObjectProperty()
    student_name = ObjectProperty()  # Variables from KV file.
    course = ObjectProperty()
    grade = ObjectProperty()
    ip = ObjectProperty()

    def __init__(self, ip):
        # Builder of the class
        super(ShowRecords, self).__init__()  # Call builder of BoxLayout since we don't use default builder
        con = mdb.connect(host=ip, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("SELECT * FROM %s"%TABLE)  # Query for select all from DB
        rows = cur.fetchall()  # fetch all rows from query
        self.ip = ip
        self.show(rows)  # call method to show results

    def show(self, rows):
        # Show results on the application screen
        self.res.text = ''  # Clean previous results
        if not rows:
            self.res.text = 'No Records'  # Error msg
        else:
            for r in rows:
                    if len(r)>3:
                        self.res.text += r[1] +'  '+r[2]+'  '+str(r[3])+ '\n' #for 'show records'
                    else:
                        self.res.text += r[0] + '  ' + str(r[1]) + '\n'  # for other functions (user_avg etc.)

    def count_users(self):
        # count the number of names for each CourseName. Note - name is not distinct since it is not restricted as unique key
        con = mdb.connect(host=self.ip, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("SELECT CourseName,COUNT(StudentName) FROM %s GROUP BY CourseName"%TABLE)
        rows=cur.fetchall()
        self.show(rows)

    def user_avg(self):
        # calculate the avg for each student
        con = mdb.connect(host=self.ip, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("select StudentName, avg(Grade) FROM %s group By StudentName "%TABLE)
        rows=cur.fetchall()
        self.show(rows)


    def good_students(self):
        # locate and show the student/s with the highest grade in math
        con = mdb.connect(host=self.ip, user=USER, passwd=PASS, db=DB)
        cur = con.cursor()
        cur.execute("SELECT StudentName, Grade FROM %s\
         WHERE grade=(SELECT MAX(Grade) FROM %s WHERE CourseName= 'Math')\
         AND CourseName='Math'"%(TABLE,TABLE))
        rows=cur.fetchall()
        self.show(rows)

    def display_input_data(self):
        # Display new form on screen
        self.clear_widgets()
        self.add_widget(InputForm())


    def out(self):
        # Close application
        sys.exit()


class KivyApp(App):
    # Run main loop uses kv file name kivy
    pass


if __name__ == '__main__':  # Set entry point
    KivyApp().run()
