from flask import Flask, request, jsonify
from db import get_user_by_username

app = Flask(__name__)

@app.route("/login", methods=["POST"])
def check_login():
    data = request.json
    if not data or "username" not in data or "password" not in data:
        return jsonify({"error": "Missing login info"}), 400
    
    username = data["username"]
    password = data["password"]

    if get_user_by_username(username) is None:
        return jsonify({"error": "Invalid username or password"}), 401
    
    user = get_user_by_username(username)

    if (user["password"] == password):
        return jsonify({
            "message": "Login successful",
            "user_id": user["id"],
            "role": user["role"]
        }), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


if __name__ == "__main__":
    app.run(debug=True)