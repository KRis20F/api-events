from flask import request, jsonify

API_KEY = 'SIUUUuuUU'  

def check_api_key():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({"error": "API key no válida"}), 403