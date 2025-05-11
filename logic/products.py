from connection import connect_to_db

def add_product():
    name = input("Enter product name: ").strip()
    description = input("Enter product description: ").strip()

    try:
        price = float(input("Enter product price: "))
        rating = float(input("Enter product rating (e.g., 4.5): "))
    except ValueError:
        print("❌ Price and rating must be numbers.")
        return

    query = "INSERT INTO products (name, description, price, rating) VALUES (%s, %s, %s, %s);"

    try:
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (name, description, price, rating))
            conn.commit()
        print("✅ Product added successfully.")
    except Exception as e:
        print("❌ Error adding product:", e)


def get_products():
    query = "SELECT * FROM products"
    try:
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        print("❌ Error fetching products:", e)
        return []