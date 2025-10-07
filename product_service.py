from flask import Flask, jsonify, request

app = Flask(__name__)

# Dummy in-memory product data
products = {
    101: {"name": "Laptop", "price": 1000},
    102: {"name": "Phone", "price": 500}
}

@app.route('/product/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product)

# Add a POST endpoint to create a product
@app.route('/product', methods=['POST'])
def create_product():
    data = request.json
    # Generate a new product ID (just an example, consider using a better ID strategy)
    product_id = max(products.keys()) + 1  
    products[product_id] = {
        "product_id": product_id,  # Add product_id to the response
        "name": data["name"],
        "price": data["price"]
    }
    return jsonify(products[product_id]), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
