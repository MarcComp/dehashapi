from flask import Flask, jsonify, request, render_template_string
from flask_cors import CORS

from runnerscript import run_hashcat_operations


app = Flask(__name__)
# Allows  CORS for all routes
CORS(app)

@app.route("/hash/<hash>", methods=['GET'])
def return_hash(hash):
    #data = {'message': 'Hello, this is a simple GET request example!'}
    
    return jsonify(run_hashcat_operations(hash))


if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=8080)