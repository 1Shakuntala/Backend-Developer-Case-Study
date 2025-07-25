from flask import request, jsonify
from app import app, db
from models import Product, Inventory

@app.route('/api/products', methods=['POST'])
def create_product():
    data = request.get_json()

    # Simple check for required fields
    if 'name' not in data or 'sku' not in data or 'price' not in data or 'warehouse_id' not in data or 'initial_quantity' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    try:
        # Create product
        product = Product(
            name=data['name'],
            sku=data['sku'],
            price=data['price'],
            warehouse_id=data['warehouse_id']
        )
        db.session.add(product)
        db.session.flush()  # Get product.id

        # Create inventory
        inventory = Inventory(
            product_id=product.id,
            warehouse_id=data['warehouse_id'],
            quantity=data['initial_quantity']
        )
        db.session.add(inventory)
        db.session.commit()

        return jsonify({"message": "Product created", "product_id": product.id}), 201

    except:
        db.session.rollback()
        return jsonify({"error": "Something went wrong"}), 500
