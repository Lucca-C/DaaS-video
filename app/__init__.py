from flask import Flask
from flask_cors import CORS
import os

# Initialize the Flask application
application = Flask(__name__)

# Set the application's debug mode
application.debug = True

# Set a random secret key for the session
application.secret_key = os.urandom(16)

# Apply CORS to the application
CORS(application)

# Import the routes (This import statement is at the bottom to avoid circular imports)
from app import routes
