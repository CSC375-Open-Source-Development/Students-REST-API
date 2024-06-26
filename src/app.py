from flask import Flask, jsonify, request, render_template, make_response
from jsonschema import ValidationError
from flask_cors import CORS
from dotenv import load_dotenv
import subprocess
from .database.student_database import StudentDatabase
from flask_expects_json import expects_json
from .api.students_api import students_api

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(students_api)

@app.errorhandler(400)
def bad_request(error):
    try:
        if isinstance(error.description, ValidationError):
            original_error = error.description
            return make_response(jsonify({'error': original_error.message}), 400)
        return error
    except Exception as e:
        print(e)
        return jsonify({ 'error': 'there was a problem processing your request' }), 500

@app.route('/', methods=['GET'])
def index():
    return jsonify({}), 200

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({ 'message': 'pong' }), 200

@app.route('/hello', methods=['POST'])
@expects_json({ 'required': ['name'], 'properties': { 'name': { 'type': 'string', 'minLength': 1 }}})
def hello():
    try:
        body = request.get_json(force=True)
        name = body['name']
        return jsonify({ 'message': f'Hello, {name}!' }), 201
    except Exception as e:
        print(e)
        return jsonify({ 'error': 'there was a problem processing your request' }), 500

@app.route('/users', methods=['POST'])
@expects_json({ 'required': ['username', 'agreedToTermsOfService'], 'properties': { 'username': { 'type': 'string' }, 'agreedToTermsOfService': { 'type': 'boolean' }}})
def users():
    try:
        body = request.get_json(force=True)
        if not body['agreedToTermsOfService']:
            return jsonify({ 'error': 'terms of service must be agreed to' }), 400
        
        if not body['username']:
            return jsonify({ 'error': 'missing username' }), 400
        
        student_database = StudentDatabase()
        if student_database.does_username_exist(body['username']):
            return jsonify({ 'error': 'username already exists' }), 400
        
        token = student_database.insert_user(body['username'])
        return jsonify({ 'token': token }), 201
    except Exception as e:
        print(e)
        return jsonify({ 'error': 'there was a problem processing your request' }), 500

@app.route('/docs', methods=['GET'])
def docs():
    return render_template('docs.html')

@app.route('/terms-of-service', methods=['GET'])
def terms_of_service():
    return render_template('terms-of-service.html')

def get_wlan_ip():
    result = subprocess.run('ipconfig',stdout=subprocess.PIPE,text=True).stdout.lower()
    scan = False
    for i in result.split('\n'):
        if 'wireless' in i: 
            scan = True
        if scan and 'ipv4' in i: 
            return i.split(':')[1].strip()

@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response

if __name__ == "__main__":
    print(f"IP Address: {get_wlan_ip()}")
    app.run(host='0.0.0.0', port=3000,  threaded=True)