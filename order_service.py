from flask import Flask, jsonify, request
import requests

app = Flask(__name__)

USER_SERVICE_URL = "http://testapp15:5001/"  # URL of the user service
PRODUCT_SERVICE_URL = "http://testapp14:5002"  # URL of the product service

@app.route('/order', methods=['POST'])
def create_order():
    order_data = request.json
    user_id = order_data.get('user_id')
    product_id = order_data.get('product_id')

    # Fetch user data from the User Service
    try:
        user_response = requests.get(f"{USER_SERVICE_URL}/user/{user_id}")
        if user_response.status_code != 200:
            return jsonify({"error": "User not found", "details": user_response.text}), 404
        user_data = user_response.json()
    except Exception as e:
        return jsonify({"error": "Failed to fetch user", "details": str(e)}), 500

    # Fetch product data from the Product Service
    try:
        product_response = requests.get(f"{PRODUCT_SERVICE_URL}/product/{product_id}")
        if product_response.status_code != 200:
            return jsonify({"error": "Product not found", "details": product_response.text}), 404
        product_data = product_response.json()
    except Exception as e:
        return jsonify({"error": "Failed to fetch product", "details": str(e)}), 500

    # If both user and product are valid, create the order
    order = {
        "order_id": 123456,  # Example static order ID, you can generate this dynamically
        "user": user_data,
        "product": product_data,
        "status": "Created"
    }

    return jsonify(order), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
