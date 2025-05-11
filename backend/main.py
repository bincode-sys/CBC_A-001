from flask import Flask, send_from_directory
from flask_restful import Api
from flask_cors import CORS
from insert_db import InsertDB
from fetch_db import FetchDB

app = Flask(__name__, static_folder="../frontend", static_url_path="")
CORS(app)  # Enable CORS for frontend requests
api = Api(app)

# Serve the frontend (index.html and other static files like suggestions_data.json)
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

# Serve other static files (e.g., suggestions_data.json)
@app.route('/<path:path>')
def serve_static(path):
    try:
        return send_from_directory(app.static_folder, path)
    except FileNotFoundError:
        return {'message': 'File not found'}, 404

# API endpoints
api.add_resource(InsertDB, '/api/calculate')
api.add_resource(FetchDB, '/api/history')

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
