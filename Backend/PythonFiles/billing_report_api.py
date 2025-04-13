from flask import Flask, request, jsonify
from flask_cors import CORS

# Initialize the Flask app
app = Flask(__name__)
CORS(app)  # Allow cross-origin requests for Angular integration

# Define the route for POST
@app.route('/api/billing', methods=['POST'])
def receive_data():
    data = request.get_json()
    print("Received data:", data)  # Print received data
    return jsonify({"message": "Data received successfully"}), 200

# Entry point of the script
if __name__ == '__main__':
    app.run(debug=True, port=5000)
