from flask import Blueprint, jsonify, request
from ..database.student_database import StudentDatabase
from flask_expects_json import expects_json

students_api = Blueprint('students_api', __name__)

@students_api.before_request
def auth():
    try:
        bearer_token = request.headers['Authorization'].strip()
        if bearer_token[0:7] != 'Bearer ':
            return jsonify({ 'error': 'missing or invalid token' }), 401
        token = bearer_token[7:]
        student_database = StudentDatabase()
        if not student_database.is_token_valid(token):
            return jsonify({ 'error': 'missing or invalid token' }), 401
    except:
        return jsonify({ 'error': 'missing or invalid token' }), 401
    
@students_api.route('/students', methods=['GET', 'POST'])
@expects_json({ 'required': ['firstName', 'lastName', 'email'], 'properties': { 'firstName': { 'type': 'string', 'minLength': 1 }, 'lastName': { 'type': 'string', 'minLength': 1 }, 'email': { 'type': 'string', 'format': 'email' }}})
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
        student_database = StudentDatabase()
        id = student_database.insert_student(student)
        student = student_database.get_student_by_id(id)
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
        
 