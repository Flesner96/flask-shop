from flask import Flask, flash, redirect, render_template, request
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
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "").strip()
        rating = request.form.get("rating", "").strip()

        errors = []

        # Validate required fields
        if not name:
            errors.append("Product name is required.")
        if not price:
            errors.append("Price is required.")
        else:
            try:
                price = float(price)
            except ValueError:
                errors.append("Price must be a number.")

        if rating:
            try:
                rating = float(rating)
            except ValueError:
                errors.append("Rating must be a number.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("add_product.html", name=name, description=description)

        # Insert into DB
        try:
            insert_product(name, description, price, rating)
            flash("Product added successfully!", "success")
            return redirect("/products")
        except Exception as e:
            flash(f"Error adding product: {e}", "error")
            return render_template("add_product.html")

    return render_template("add_product.html")

@app.route("/add_client", methods=["GET", "POST"])
def create_client():
    if request.method == "POST":
        first_name = request.form.get("first_name", "").strip()
        last_name = request.form.get("last_name", "").strip()

        errors = []
        if not first_name:
            errors.append("First name is required.")
        if not last_name:
            errors.append("Last name is required.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("add_client.html", first_name=first_name, last_name=last_name)

        try:
            insert_client(first_name, last_name)
            flash("Client added successfully!", "success")
            return redirect("/clients")
        except Exception as e:
            flash(f"Error adding client: {e}", "error")
            return render_template("add_client.html")

    return render_template("add_client.html")

@app.route("/add_order", methods=["GET", "POST"])
def create_order():
    if request.method == "POST":
        client_id = request.form.get("client_id", "").strip()
        order_details = request.form.get("order_details", "").strip()

        errors = []
        if not client_id:
            errors.append("Client ID is required.")
        else:
            try:
                client_id = int(client_id)
            except ValueError:
                errors.append("Client ID must be a number.")

        if not order_details:
            errors.append("Order details are required.")

        if errors:
            for error in errors:
                flash(error, "error")
            return render_template("add_order.html", client_id=client_id, order_details=order_details)

        try:
            insert_order(client_id, order_details)
            flash("Order added successfully!", "success")
            return redirect("/orders")
        except Exception as e:
            flash(f"Error adding order: {e}", "error")
            return render_template("add_order.html")

    return render_template("add_order.html")

if __name__ == "__main__":
    app.run(debug=True)
