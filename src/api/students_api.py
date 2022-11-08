from flask import Blueprint, jsonify, request
from ..database.student_database import StudentDatabase
from urllib.parse import urlparse

students_api = Blueprint('students_api', __name__)

@students_api.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
       return get_all_students()
    elif request.method == 'POST':
        body = request.get_json(force=True)
        return create_student(body)

def get_all_students():
    try:
        student_database = StudentDatabase()
        students = student_database.get_all_students()
        return jsonify(students), 200
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

def create_student(student):
    try:
        required_fields = ['firstName', 'lastName', 'email']
        for required_field in required_fields:
            if not required_field in student or not student[required_field]:
                return jsonify({ 'error': f'missing \'{required_field}\' value in request' }), 400 
 
        student_database = StudentDatabase()
        student_database.insert_student(student)
        return jsonify(student), 201
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500

@students_api.route('/students/<id>', methods=['GET', 'PUT', 'DELETE'])
def students_id(id):
    try:
        student_database = StudentDatabase()
        student = student_database.get_student_by_id(id)
        if not student:
            return jsonify({ 'error': f'Student Not Found: {id}' }), 404
    except Exception as e:
        return jsonify({ 'error', str(e) }), 500

    if request.method == 'GET':
        return jsonify(student), 200

    elif request.method == 'PUT':
        body = request.get_json(force=True)
        return update_student(id, body)
    
    elif request.method == 'DELETE':
        return delete_student(id)

def update_student(id, student):
    try:
        required_fields = ['firstName', 'lastName', 'email']
        for required_field in required_fields:
            if not required_field in student or not student[required_field]:
                return jsonify({ 'error': f'missing \'{required_field}\' value in request' }), 400 
    
        student_database = StudentDatabase()
        student_database.update_student(id, student)
        return jsonify(student), 200
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500


def delete_student(id):
    try:
        student_database = StudentDatabase()
        student_database.delete_student(id)
        return jsonify({ 'message': f'Successfully deleted student {id}'}), 200
    except Exception as e:
        return jsonify({ 'error': str(e) }), 500
        
 