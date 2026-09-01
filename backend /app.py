"""
NOVA E-Commerce — Flask backend
================================
A REST API backend for the NOVA storefront, backed by SQL (SQLite by
default via SQLAlchemy — point SQLALCHEMY_DATABASE_URI at Postgres/MySQL
in production and nothing else needs to change).

Run:
    pip install -r requirements.txt
    python app.py

The API listens on http://localhost:5000
"""
import os
from functools import wraps

from flask import Flask, request, jsonify, session
from flask_cors import CORS

from models import db, Product, User, CartItem, Order, OrderItem
from seed_data import PRODUCTS

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(BASE_DIR, "nova.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.environ.get("NOVA_SECRET_KEY", "dev-secret-change-me")
# Allow the session cookie to be sent from a separate frontend origin (e.g. localhost:3000)
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

db.init_app(app)
CORS(app, supports_credentials=True)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def login_required(view_fn):
    @wraps(view_fn)
    def wrapped(*args, **kwargs):
        if not session.get("user_id"):
            return jsonify({"error": "Authentication required"}), 401
        return view_fn(*args, **kwargs)
    return wrapped


def current_user():
    uid = session.get("user_id")
    return User.query.get(uid) if uid else None


def seed_database():
    """Populate the products table once, on first run."""
    if Product.query.first():
        return
    for p in PRODUCTS:
        db.session.add(Product(
            id=p["id"], name=p["name"], category=p["category"], price=p["price"],
            rating=p["rating"], reviews=p["reviews"], badge=p["badge"],
            image=p["image"], description=p["description"], stock=p.get("stock", 50),
        ))
    db.session.commit()


# ---------------------------------------------------------------------------
# Health check
# ---------------------------------------------------------------------------
@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "service": "nova-backend"})


# ---------------------------------------------------------------------------
# Products
# ---------------------------------------------------------------------------
@app.route("/api/products", methods=["GET"])
def list_products():
    """Supports ?search=&category=&sort=price_asc|price_desc|rating"""
    query = Product.query

    search = request.args.get("search", "").strip()
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))

    category = request.args.get("category", "all")
    if category and category != "all":
        query = query.filter_by(category=category)

    sort = request.args.get("sort")
    if sort == "price_asc":
        query = query.order_by(Product.price.asc())
    elif sort == "price_desc":
        query = query.order_by(Product.price.desc())
    elif sort == "rating":
        query = query.order_by(Product.rating.desc())

    products = query.all()
    return jsonify({
        "count": len(products),
        "products": [p.to_dict() for p in products],
    })


@app.route("/api/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404
    return jsonify(product.to_dict())


@app.route("/api/categories", methods=["GET"])
def list_categories():
    rows = db.session.query(Product.category, db.func.count(Product.id)).group_by(Product.category).all()
    return jsonify({"categories": [{"name": c, "count": n} for c, n in rows]})


# ---------------------------------------------------------------------------
# Auth
# ---------------------------------------------------------------------------
@app.route("/api/auth/register", methods=["POST"])
def register():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""
    first_name = data.get("first_name", "")
    last_name = data.get("last_name", "")

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400
    if len(password) < 6:
        return jsonify({"error": "password must be at least 6 characters"}), 400
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "an account with this email already exists"}), 409

    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id
    return jsonify({"user": user.to_dict()}), 201


@app.route("/api/auth/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "invalid email or password"}), 401

    session["user_id"] = user.id
    return jsonify({"user": user.to_dict()})


@app.route("/api/auth/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "logged out"})


@app.route("/api/auth/me", methods=["GET"])
def me():
    user = current_user()
    if not user:
        return jsonify({"user": None})
    return jsonify({"user": user.to_dict()})


# ---------------------------------------------------------------------------
# Cart  (persisted per logged-in user in SQL)
# ---------------------------------------------------------------------------
@app.route("/api/cart", methods=["GET"])
@login_required
def get_cart():
    items = CartItem.query.filter_by(user_id=session["user_id"]).all()
    total = sum(i.product.price * i.quantity for i in items if i.product)
    return jsonify({
        "items": [i.to_dict() for i in items],
        "total": round(total, 2),
        "count": sum(i.quantity for i in items),
    })


@app.route("/api/cart/add", methods=["POST"])
@login_required
def add_to_cart():
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    product = Product.query.get(product_id)
    if not product:
        return jsonify({"error": "Product not found"}), 404

    item = CartItem.query.filter_by(user_id=session["user_id"], product_id=product_id).first()
    if item:
        item.quantity += quantity
    else:
        item = CartItem(user_id=session["user_id"], product_id=product_id, quantity=quantity)
        db.session.add(item)
    db.session.commit()
    return jsonify(item.to_dict()), 201


@app.route("/api/cart/update", methods=["POST"])
@login_required
def update_cart_item():
    data = request.get_json(silent=True) or {}
    product_id = data.get("product_id")
    quantity = int(data.get("quantity", 1))

    item = CartItem.query.filter_by(user_id=session["user_id"], product_id=product_id).first()
    if not item:
        return jsonify({"error": "Item not in cart"}), 404

    if quantity <= 0:
        db.session.delete(item)
        db.session.commit()
        return jsonify({"message": "Item removed"})

    item.quantity = quantity
    db.session.commit()
    return jsonify(item.to_dict())


@app.route("/api/cart/remove/<int:product_id>", methods=["DELETE"])
@login_required
def remove_from_cart(product_id):
    item = CartItem.query.filter_by(user_id=session["user_id"], product_id=product_id).first()
    if not item:
        return jsonify({"error": "Item not in cart"}), 404
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item removed"})


@app.route("/api/cart/clear", methods=["POST"])
@login_required
def clear_cart():
    CartItem.query.filter_by(user_id=session["user_id"]).delete()
    db.session.commit()
    return jsonify({"message": "Cart cleared"})


# ---------------------------------------------------------------------------
# Checkout / Orders
# ---------------------------------------------------------------------------
@app.route("/api/checkout", methods=["POST"])
@login_required
def checkout():
    data = request.get_json(silent=True) or {}
    required = ["first_name", "last_name", "email", "street_address", "city", "state", "zip_code"]
    missing = [f for f in required if not data.get(f)]
    if missing:
        return jsonify({"error": f"Missing fields: {', '.join(missing)}"}), 400

    cart_items = CartItem.query.filter_by(user_id=session["user_id"]).all()
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    # Validate stock and compute total
    total = 0
    for ci in cart_items:
        if not ci.product or ci.product.stock < ci.quantity:
            return jsonify({"error": f"'{ci.product.name if ci.product else 'item'}' is out of stock"}), 409
        total += ci.product.price * ci.quantity

    order = Order(
        user_id=session["user_id"], status="placed", total=round(total, 2),
        first_name=data["first_name"], last_name=data["last_name"], email=data["email"],
        street_address=data["street_address"], city=data["city"], state=data["state"],
        zip_code=data["zip_code"],
    )
    db.session.add(order)
    db.session.flush()  # get order.id before commit

    for ci in cart_items:
        db.session.add(OrderItem(
            order_id=order.id, product_id=ci.product_id, product_name=ci.product.name,
            price=ci.product.price, quantity=ci.quantity,
        ))
        ci.product.stock -= ci.quantity
        db.session.delete(ci)  # clear the cart

    db.session.commit()
    return jsonify({"order": order.to_dict()}), 201


@app.route("/api/orders", methods=["GET"])
@login_required
def list_orders():
    orders = Order.query.filter_by(user_id=session["user_id"]).order_by(Order.created_at.desc()).all()
    return jsonify({"orders": [o.to_dict() for o in orders]})


@app.route("/api/orders/<int:order_id>", methods=["GET"])
@login_required
def get_order(order_id):
    order = Order.query.filter_by(id=order_id, user_id=session["user_id"]).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404
    return jsonify(order.to_dict())


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------
with app.app_context():
    db.create_all()
    seed_database()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
