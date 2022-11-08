from .sqlite_database import SqliteDatabase
import os

class StudentDatabase(SqliteDatabase):

    def __init__(self):
        super().__init__(os.getenv('STUDENT_DATABASE'))

    def student_row_to_json(self, student):
        return {
            'id': student[0],
            'firstName': student[1],
            'lastName': student[2],
            'email': student[3]
        }
        
    def get_all_students(self):
        students = self.run_query('SELECT id, first_name, last_name, email FROM Students')
        return [self.student_row_to_json(student) for student in students]

    def get_student_by_id(self, id):
        students = self.run_query('SELECT id, first_name, last_name, email FROM Students WHERE id = ?', [id])
        results = students.fetchall()
        if len(results) > 0:
            return self.student_row_to_json(results[0])
        return None

    def insert_student(self, student):
        first_name = student['firstName']
        last_name = student['lastName']
        email = student['email']
        self.run_non_query('INSERT INTO Students (first_name, last_name, email) VALUES (?, ?, ?)', [first_name, last_name, email])

    def update_student(self, id, student):
        first_name = student['firstName']
        last_name = student['lastName']
        email = student['email']
        self.run_non_query('UPDATE Students SET first_name = ?, last_name = ?, email = ? WHERE id = ?', [first_name, last_name, email, id])

    def delete_student(self, id):
        self.run_non_query('DELETE FROM Students WHERE id = ?', [id])