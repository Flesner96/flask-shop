from flask import Flask, redirect, render_template, request
from logic.products import get_products, insert_product
from logic.clients import get_clients, insert_client
from logic.orders import get_orders, insert_order

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
        name = request.form["name"]
        description = request.form["description"]
        price = request.form["price"]
        rating = request.form["rating"]

        insert_product(name, description, price, rating)
        return redirect("/products")
    return render_template("add_product.html")

@app.route("/add_client", methods=["GET", "POST"])
def create_client():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        insert_client(first_name, last_name)
        return redirect("/clients")
    return render_template("add_client.html")

@app.route("/add_order", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        client_id = request.form["client_id"]
        order_details = request.form["order_details"]
        insert_order(client_id, order_details)
        return redirect("/orders")
    return render_template("add_order.html")

if __name__ == "__main__":
    app.run(debug=True)
