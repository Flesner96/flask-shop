from connection import connect_to_db

# def add_product():
#     name = input("Enter product name: ").strip()
#     description = input("Enter product description: ").strip()

#     try:
#         price = float(input("Enter product price: "))
#         rating = float(input("Enter product rating (e.g., 4.5): "))
#     except ValueError:
#         print("❌ Price and rating must be numbers.")
#         return

#     query = "INSERT INTO products (name, description, price, rating) VALUES (%s, %s, %s, %s);"

#     try:
#         with connect_to_db() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute(query, (name, description, price, rating))
#             conn.commit()
#         print("✅ Product added successfully.")
#     except Exception as e:
#         print("❌ Error adding product:", e)


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
    
def insert_product(name, description, price, rating):
    query = """
        INSERT INTO products (name, description, price, rating)
        VALUES (%s, %s, %s, %s)
    """
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (name, description, price, rating))
        conn.commit()

def get_product_by_id(product_id):
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            row = cur.fetchone()
            return dict(zip([desc[0] for desc in cur.description], row)) if row else None

def update_product(product_id, name, description, price, rating):
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                UPDATE products
                SET name = %s, description = %s, price = %s, rating = %s
                WHERE id = %s
            """, (name, description, price, rating, product_id))
        conn.commit()

def delete_product_by_id(product_id):
    with connect_to_db() as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM products WHERE id = %s", (product_id,))
        conn.commit()


def search_products(name=None, min_price=None, max_price=None, limit=10, offset=0):
    query = "SELECT * FROM products WHERE TRUE"
    params = []

    if name:
        query += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if min_price:
        query += " AND price >= %s"
        params.append(min_price)
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)

    query += " ORDER BY id LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
        

def count_products(name=None, min_price=None, max_price=None):
    query = "SELECT COUNT(*) FROM products WHERE TRUE"
    params = []

    if name:
        query += " AND name ILIKE %s"
        params.append(f"%{name}%")
    if min_price:
        query += " AND price >= %s"
        params.append(min_price)
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)

    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()[0]
