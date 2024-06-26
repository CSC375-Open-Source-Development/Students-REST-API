from .sqlite_database import SqliteDatabase
import os
import uuid

class StudentDatabase(SqliteDatabase):

    def __init__(self):
        super().__init__(os.getenv('STUDENT_DATABASE'))

    def user_row_to_json(self, user):
        return {
            'id': user[0],
            'username': user[1],
            'token': user[2]
        }

    def does_username_exist(self, username):
        users = self.run_query('SELECT * FROM Users WHERE username = ?', [username])
        return not len(users.fetchall()) == 0

    def insert_user(self, username):
        token = uuid.uuid4()
        self.run_non_query('INSERT INTO Users (username, token) VALUES (?, ?)', [username, str(token)])
        return token
    
    def get_user_by_token(self, token):
        users = self.run_non_query('SELECT * FROM Users WHERE token = ?', [token])
        results = users.fetchall()
        if len(results) == 1:
            return self.user_row_to_json(results[0])
        return None

    def is_token_valid(self, token):
        users = self.run_query('SELECT id, username, token FROM Users WHERE token = ?', [token])
        return len(users.fetchall()) == 1

    def student_row_to_json(self, student):
        return {
            'id': student[0],
            'firstName': student[1],
            'lastName': student[2],
            'email': student[3],
            'major': student[4],
            'createdBy': student[5]
        }
        
    def get_all_students(self):
        students = self.run_query('SELECT id, first_name, last_name, email, major, created_by FROM Students')
        return [self.student_row_to_json(student) for student in students]
    
    def get_all_students_created_by_user(self, username):
        students = self.run_query('SELECT id, first_name, last_name, email, major, created_by FROM Students WHERE created_by = ?', [username])
        return [self.student_row_to_json(student) for student in students]

    def get_student_by_id(self, id):
        students = self.run_query('SELECT id, first_name, last_name, email, major, created_by FROM Students WHERE id = ?', [id])
        results = students.fetchall()
        if len(results) > 0:
            return self.student_row_to_json(results[0])
        return None
    
    def get_all_students_by_email(self, email):
        students = self.run_query('SELECT id, first_name, last_name, email, major, created_by FROM Students WHERE email = ?', [email])
        return [self.student_row_to_json(student) for student in students]
    
    # exclude field is to pass an id of a student to not include in this check
    # useful for PUT operation in the case the email of the given student has not changed -- it ensures it does not count itself as the email already existing
    def does_student_with_email_already_exist(self, email, exclude=None):
        query = 'SELECT id, first_name, last_name, email, major, created_by FROM Students WHERE email = ?'
        params = [email]
        if exclude:
            query += ' AND id != ?'
            params.append(exclude)
        students = self.run_query(query, params)
        return len(students.fetchall()) > 0       

    def insert_student(self, student, username):
        first_name = student['firstName']
        last_name = student['lastName']
        email = student['email']
        major = student['major']
        result = self.run_non_query('INSERT INTO Students (first_name, last_name, email, major, created_by) VALUES (?, ?, ?, ?, ?)', [first_name, last_name, email, major, username])
        return result.lastrowid

    def update_student(self, id, student):
        first_name = student['firstName']
        last_name = student['lastName']
        email = student['email']
        major = student['major']
        self.run_non_query('UPDATE Students SET first_name = ?, last_name = ?, email = ?, major = ? WHERE id = ?', [first_name, last_name, email, major, id])

    def delete_student(self, id):
        self.run_non_query('DELETE FROM Students WHERE id = ?', [id])