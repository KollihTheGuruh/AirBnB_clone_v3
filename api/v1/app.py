#!/usr/bin/python3
"""
app.py to connect to API. app entry point
"""

import os
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
from flasgger import Swagger
from werkzeug.exceptions import HTTPException

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(app_views)
app.url_map.strict_slashes = False

cors = CORS(app, resources={
            r'/*': {'origins': os.getenv('HBNB_API_HOST', '0.0.0.0')}})

# Note: You had this line twice in your original script. You should only need to register the blueprint once.
# app.register_blueprint(app_views)

@app.teardown_appcontext
def teardown(code):
    """
    teardown_appcontext method that closes the storage
    """
    storage.close()

@app.errorhandler(404)
def page_404_not_found(e):
    """method for 404 errors.
    Returns a JSON object with an error message and the status code.
    """
    return jsonify({'error': 'Not found'}), 404

# We removed the setup_global_errors function as it doesn't seem to be used or defined properly with a global_error_handler.

if __name__ == "__main__":
    app.run(host=os.getenv('HBNB_API_HOST', '0.0.0.0'),
            port=int(os.getenv('HBNB_API_PORT', '5000')),
            threaded=True)
