from flask import Flask, redirect, render_template, request
from connection import connect_to_db
from logic.products import get_products
from logic.clients import get_clients
from logic.orders import get_orders

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

        query = """
            INSERT INTO products (name, description, price, rating)
            VALUES (%s, %s, %s, %s);
        """
        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (name, description, price, rating))
                conn.commit()
        except Exception as e:
            return f"❌ Error adding product: {e}"

        return redirect("/products")
    return render_template("add_product.html")

@app.route("/add_client", methods=["GET", "POST"])
def create_client():
    if request.method == "POST":
        first_name = request.form["first_name"]
        last_name = request.form["last_name"]

        query = "INSERT INTO client (name, surname) VALUES (%s, %s);"
        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (first_name, last_name))
                conn.commit()
        except Exception as e:
            return f"❌ Error adding client: {e}"

        return redirect("/clients")
    return render_template("add_client.html")

@app.route("/add_order", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        client_id = request.form["client_id"]
        order_details = request.form["order_details"]

        query = "INSERT INTO orders (customer_id, order_details) VALUES (%s, %s);"
        try:
            with connect_to_db() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(query, (client_id, order_details))
                conn.commit()
        except Exception as e:
            return f"❌ Error adding order: {e}"

        return redirect("/orders")
    return render_template("add_order.html")

if __name__ == "__main__":
    app.run(debug=True)
