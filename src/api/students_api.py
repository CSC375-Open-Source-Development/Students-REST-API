from flask import Blueprint, jsonify, request
from ..database.student_database import StudentDatabase
from flask_expects_json import expects_json
import re

students_api = Blueprint('students_api', __name__)

email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

# Before any request to the below routes, verify that the token supplied in the header is valid
@students_api.before_request
def auth():
    try:
        token = request.headers['Authorization'].strip()
        student_database = StudentDatabase()
        if not student_database.is_token_valid(token):
            return jsonify({ 'error': 'missing or invalid token' }), 401
    except:
        return jsonify({ 'error': 'missing or invalid token' }), 401
    
@students_api.route('/students', methods=['GET', 'POST'])
@expects_json({ 'required': ['firstName', 'lastName', 'email'], 'properties': { 'firstName': { 'type': 'string', 'minLength': 1 }, 'lastName': { 'type': 'string', 'minLength': 1 }, 'email': { 'type': 'string' }, 'major': { 'type': 'string', 'minLength': 1 }}}, ignore_for=['GET'])
def students():
    try:
        if request.method == 'GET':
            created_by = request.args.get('createdBy')
            if created_by != None:
                return get_all_students_created_by_user(created_by)
            else:
                return get_all_students()
        elif request.method == 'POST':
            body = request.get_json(force=True)
            return create_student(body)
    except Exception as e:
        print(e)
        return jsonify({ 'error': 'there was a problem processing your request' }), 500

def get_all_students():
    student_database = StudentDatabase()
    students = student_database.get_all_students()
    return jsonify(students), 200
    
def get_all_students_created_by_user(username):
    student_database = StudentDatabase()
    students = student_database.get_all_students_created_by_user(username)
    return jsonify(students), 200

def create_student(request_body):
    student_database = StudentDatabase()
    if not re.match(email_pattern, request_body['email']):
        return jsonify({ 'error': 'invalid email address format' }), 400
    if student_database.does_student_with_email_already_exist(request_body['email']):
        return jsonify({ 'error': 'specified email is already assigned to another student' }), 400
    token = request.headers['Authorization'].strip()
    user = student_database.get_user_by_token(token)
    if 'major' not in request_body:
        request_body['major'] = None
    id = student_database.insert_student(request_body, user['username'])
    created_student = student_database.get_student_by_id(id)
    return jsonify(created_student), 201

@students_api.route('/students/<id>', methods=['GET', 'PUT', 'DELETE'])
@expects_json({ 'required': ['firstName', 'lastName', 'email', 'major'], 'properties': { 'firstName': { 'type': 'string', 'minLength': 1 }, 'lastName': { 'type': 'string', 'minLength': 1 }, 'email': { 'type': 'string' }, 'major': { 'type': ['string', 'null'] }}}, ignore_for=['GET', 'DELETE'])
def students_id(id):
    try:
        student_database = StudentDatabase()
        existing_student = student_database.get_student_by_id(id)
        if not existing_student:
            return jsonify({ 'error': 'Student Not Found' }), 404
        if request.method == 'GET':
            return jsonify(existing_student), 200
        elif request.method == 'PUT':
            request_body = request.get_json(force=True)
            if not re.match(email_pattern, request_body['email']):
                return jsonify({ 'error': 'invalid email address format' }), 400
            return update_student(id, existing_student, request_body)
        elif request.method == 'DELETE':
            return delete_student(id, existing_student)
    except Exception as e:
        print(e)
        return jsonify({ 'error': 'there was a problem processing your request' }), 500

def update_student(id, existing_student, request_body):
    student_database = StudentDatabase()
    if student_database.does_student_with_email_already_exist(request_body['email'], exclude=id):
        return jsonify({ 'error': 'specified email is already assigned to another student' }), 400
    token = request.headers['Authorization'].strip()
    user = student_database.get_user_by_token(token)
    if user['username'] != existing_student['createdBy']:
        return jsonify({ 'message': 'you do not have permission to update this student' }), 403
    student_database.update_student(id, request_body)
    updated_student = student_database.get_student_by_id(id)
    return jsonify(updated_student), 200

def delete_student(id, existing_student):
    student_database = StudentDatabase()
    token = request.headers['Authorization'].strip()
    user = student_database.get_user_by_token(token)
    if user['username'] != existing_student['createdBy']:
        return jsonify({ 'message': 'you do not have permission to delete this student' }), 403
    student_database.delete_student(id)
    return jsonify({ 'message': 'Successfully deleted student' }), 200
        
 