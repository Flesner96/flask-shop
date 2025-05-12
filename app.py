from functools import wraps
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from logic.products import count_products, delete_product_by_id, get_product_by_id, insert_product, search_products, update_product
from logic.clients import count_clients, insert_client, search_clients
from logic.orders import count_orders,  insert_order, search_orders

app = Flask(__name__)
app.secret_key = "your_secret_key_here"  


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Simple check — replace with real auth later
        if username == "admin" and password == "admin123":
            session["logged_in"] = True
            flash("Logged in successfully.", "success")
            return redirect("/")
        else:
            flash("Invalid credentials.", "error")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("Logged out.", "success")
    return redirect("/login")


def login_required(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Login required to access this page.", "error")
            return redirect("/login")
        return route_func(*args, **kwargs)
    return wrapper

def api_login_required(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            return jsonify({"error": "Unauthorized"}), 401
        return route_func(*args, **kwargs)
    return wrapper


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/products")
@login_required
def show_products():
    name = request.args.get("name")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)
    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    products = search_products(name, min_price, max_price, limit=per_page, offset=offset)
    total = count_products(name, min_price, max_price)
    has_next = offset + per_page < total

    return render_template(
        "products.html",
        products=products,
        page=page,
        name=name or "",
        min_price=min_price,
        max_price=max_price,
        has_next=has_next
    )


@app.route("/clients")
@login_required
def show_clients():
    first_name = request.args.get("first_name", "")
    last_name = request.args.get("last_name", "")
    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    clients = search_clients(first_name, last_name, limit=per_page, offset=offset)
    total = count_clients(first_name, last_name)
    has_next = offset + per_page < total

    return render_template(
        "clients.html",
        clients=clients,
        page=page,
        first_name=first_name,
        last_name=last_name,
        has_next=has_next
    )


@app.route("/orders")
@login_required
def show_orders():
    client_id = request.args.get("client_id", type=int)
    date = request.args.get("date")
    page = request.args.get("page", 1, type=int)
    per_page = 5
    offset = (page - 1) * per_page

    orders = search_orders(client_id, date, limit=per_page, offset=offset)
    total = count_orders(client_id, date)
    has_next = offset + per_page < total

    return render_template(
        "orders.html",
        orders=orders,
        client_id=client_id or "",
        date=date or "",
        page=page,
        has_next=has_next
    )


@app.route("/add_product", methods=["GET", "POST"])
@login_required
def create_product():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "").strip()
        rating = request.form.get("rating", "").strip()

        errors = []

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

        try:
            insert_product(name, description, price, rating)
            flash("Product added successfully!", "success")
            return redirect("/products")
        except Exception as e:
            flash(f"Error adding product: {e}", "error")
            return render_template("add_product.html")

    return render_template("add_product.html")


@app.route("/add_client", methods=["GET", "POST"])
@login_required
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
@login_required
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


@app.route("/edit_product/<int:product_id>", methods=["GET", "POST"])
@login_required
def edit_product(product_id):
    product = get_product_by_id(product_id)  
    if not product:
        flash("Product not found.", "error")
        return redirect("/products")

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", "").strip()
        rating = request.form.get("rating", "").strip()

        errors = []
        if not name:
            errors.append("Name is required.")
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
            for err in errors:
                flash(err, "error")
            return render_template("edit_product.html", product=product)

        update_product(product_id, name, description, price, rating)
        flash("Product updated.", "success")
        return redirect("/products")

    return render_template("edit_product.html", product=product)


@app.route("/delete_product/<int:product_id>", methods=["POST"])
@login_required
def delete_product(product_id):
    try:
        delete_product_by_id(product_id)
        flash("Product deleted.", "success")
    except Exception as e:
        flash(f"Error deleting product: {e}", "error")
    return redirect("/products")


@app.route("/api/products")
@api_login_required
def api_products():
    name = request.args.get("name")
    min_price = request.args.get("min_price", type=float)
    max_price = request.args.get("max_price", type=float)

    products = search_products(name, min_price, max_price, limit=1000, offset=0)

    product_list = [
        {
            "id": p[0],
            "name": p[1],
            "description": p[2],
            "price": float(p[3]),
            "rating": float(p[4]) if p[4] is not None else None
        }
        for p in products
    ]
    return jsonify(product_list)


@app.route("/api/clients")
@api_login_required
def api_clients():
    first_name = request.args.get("first_name")
    last_name = request.args.get("last_name")

    clients = search_clients(first_name, last_name, limit=1000, offset=0)

    client_list = [
        {
            "id": c[0],
            "first_name": c[1],
            "last_name": c[2]
        }
        for c in clients
    ]
    return jsonify(client_list)


@app.route("/api/orders")
@api_login_required
def api_orders():
    client_id = request.args.get("client_id", type=int)
    date = request.args.get("date")

    orders = search_orders(client_id, date, limit=1000, offset=0)

    order_list = [
        {
            "id": o[0],
            "client_id": o[1],
            "details": o[2],
            "created_at": o[3].isoformat() if o[3] else None
        }
        for o in orders
    ]
    return jsonify(order_list)

if __name__ == "__main__":
    app.run(debug=True)
