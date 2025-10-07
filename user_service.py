from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy in-memory user data
users = {
    1: {"username": "john_doe", "email": "john@example.com"},
    2: {"username": "jane_smith", "email": "jane@example.com"}
}

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user)

# Add a POST endpoint to create a user
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    # Generate a new user ID (just an example, consider using a better ID strategy)
    user_id = max(users.keys()) + 1  
    users[user_id] = {
        "user_id": user_id,  # Add user_id to the response
        "username": data["username"],
        "email": data["email"]
    }
    return jsonify(users[user_id]), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
