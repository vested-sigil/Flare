from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Back4App API URL
B4A_API_URL = "https://parseapi.back4app.com/classes/"

# Headers for Back4App API
headers = {
    "X-Parse-Application-Id": os.getenv("BACK4APP_APP_ID"),
    "X-Parse-REST-API-Key": os.getenv("BACK4APP_REST_API_KEY"),
    "Content-Type": "application/json"
}

def create_object(class_name, data):
    response = requests.post(B4A_API_URL + class_name, headers=headers, json=data)
    return response.json()

def read_objects(class_name, query=None):
    response = requests.get(B4A_API_URL + class_name, headers=headers, params=query)
    return response.json()

def update_object(class_name, object_id, data):
    response = requests.put(B4A_API_URL + class_name + '/' + object_id, headers=headers, json=data)
    return response.json()

def delete_object(class_name, object_id):
    response = requests.delete(B4A_API_URL + class_name + '/' + object_id, headers=headers)
    return response.json()

@app.route('/create/<class_name>', methods=['POST'])
def create(class_name):
    data = request.json
    result = create_object(class_name, data)
    return jsonify(result)

@app.route('/read/<class_name>', methods=['GET'])
def read(class_name):
    query = request.args
    result = read_objects(class_name, query)
    return jsonify(result)

@app.route('/update/<class_name>/<object_id>', methods=['PUT'])
def update(class_name, object_id):
    data = request.json
    result = update_object(class_name, object_id, data)
    return jsonify(result)

@app.route('/delete/<class_name>/<object_id>', methods=['DELETE'])
def delete(class_name, object_id):
    result = delete_object(class_name, object_id)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
