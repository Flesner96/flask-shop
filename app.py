from flask import Flask, render_template, redirect, request
from logic.products import get_products, add_product
from logic.clients import get_clients, add_client
from logic.orders import get_orders, add_order

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/products")
def show_products():
    return render_template("products.html", products=get_products())

@app.route("/clients")
def show_clients():
    return render_template("clients.html", clients=get_clients())

@app.route("/orders")
def show_orders():
    return render_template("orders.html", orders=get_orders())

@app.route("/add_product", methods=["GET", "POST"])
def create_product():
    if request.method == "POST":
        add_product()  
        return redirect("/products")
    return render_template("add_product.html")

@app.route("/add_client", methods=["GET", "POST"])
def create_client():
    if request.method == "POST":
        add_client()  
        return redirect("/clients")
    return render_template("add_client.html")

@app.route("/add_order", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        add_order()  
        return redirect("/orders")
    return render_template("add_order.html")

if __name__ == "__main__":
    app.run(debug=True)
