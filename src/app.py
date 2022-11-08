from flask import Flask, jsonify, request
from flask_cors import CORS
from dotenv import load_dotenv
import subprocess
from .api.students_api import students_api
from bs4 import BeautifulSoup

load_dotenv()

app = Flask(__name__)
CORS(app)

app.register_blueprint(students_api)

@app.route('/ping', methods=['GET'])
def ping():
    return jsonify({ 'message': 'pong' }), 200

@app.route('/hello', methods=['POST'])
def hello():
    body = request.get_json(force=True)

    if 'name' not in body or not body['name']:
        return jsonify({ 'error': f'missing \'name\' value in request' }), 400 

    name = body['name']
    return jsonify({ 'message': f'Hello, {name}!' }), 200

@app.route('/docs', methods=['GET'])
def docs():
    with open('./resources/docs.html') as docs_html_file:
        docs_html = BeautifulSoup(docs_html_file, 'html.parser')
    return str(docs_html), 200

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
    app.run(host=get_wlan_ip(), port=5000,  threaded=True)