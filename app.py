from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///inventory.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- MODELS ----------------
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)

class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    total_amount = db.Column(db.Float, nullable=False)

# ---------------- ROUTES ----------------
@app.route('/')
def home():
    return "<h2>Welcome to Inventory Billing System</h2><p>Use /add_customer, /add_product, /create_bill etc.</p>"

# ---- CUSTOMER ROUTES ----
@app.route('/add_customer/<name>')
def add_customer(name):
    new_customer = Customer(name=name)
    db.session.add(new_customer)
    db.session.commit()
    return f"Customer '{name}' added successfully!"

@app.route('/customers')
def get_customers():
    customers = Customer.query.all()
    customer_list = [f"ID: {c.id} | Name: {c.name}" for c in customers]
    return "<br>".join(customer_list)

# ---- PRODUCT ROUTES ----
@app.route('/add_product/<name>/<int:quantity>/<float:price>')
def add_product(name, quantity, price):
    new_product = Product(name=name, quantity=quantity, price=price)
    db.session.add(new_product)
    db.session.commit()
    return f"Product {name} added successfully with quantity {quantity} and price ₹{price}!"

@app.route('/products')
def get_products():
    products = Product.query.all()
    product_list = [f"{p.name} | Qty: {p.quantity} | Price: ₹{p.price}" for p in products]
    return "<br>".join(product_list)

# ---- BILL ROUTES ----
@app.route('/create_bill/<int:customer_id>/<float:amount>')
def create_bill(customer_id, amount):
    new_bill = Bill(customer_id=customer_id, total_amount=amount)
    db.session.add(new_bill)
    db.session.commit()
    return f"Bill of ₹{amount} created for Customer ID {customer_id}!"

@app.route('/bills')
def get_bills():
    bills = Bill.query.all()
    bill_list = [f"Bill ID: {b.id} | Customer ID: {b.customer_id} | Amount: ₹{b.total_amount}" for b in bills]
    return "<br>".join(bill_list)

# ---- DASHBOARD ----
@app.route('/dashboard')
def dashboard():
    total_customers = Customer.query.count()
    total_products = Product.query.count()
    total_bills = Bill.query.count()
    total_revenue = db.session.query(db.func.sum(Bill.total_amount)).scalar() or 0

    return f"""
    <h2>📊 Dashboard</h2>
    <p>Total Customers: {total_customers}</p>
    <p>Total Products: {total_products}</p>
    <p>Total Bills: {total_bills}</p>
    <p>Total Revenue: ₹{total_revenue}</p>
    """

# ---------------- RUN ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)






