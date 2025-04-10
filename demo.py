from flask import Flask,request, jsonify
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
db = SQLAlchemy




@app.route("/", methods=["GET"])
def index():
 return "Hello, World!"


