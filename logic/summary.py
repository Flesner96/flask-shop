from connection import connect_to_db

def get_counts():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM products")
    product_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM client")
    client_count = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM orders")
    order_count = cursor.fetchone()[0]
    conn.close()
    return product_count, client_count, order_count


def get_recent_orders(limit=3):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT o.id, o.customer_id, c.name, c.surname, o.order_details, o.created_at
        FROM orders o
        JOIN client c ON o.customer_id = c.id
        ORDER BY o.created_at DESC
        LIMIT %s
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_latest_product():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, price, rating, created_at
        FROM products
        ORDER BY created_at DESC
        LIMIT 1
    """)
    latest = cursor.fetchone()
    conn.close()
    return latest


def get_best_rated_product():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT id, name, price, rating
        FROM products
        ORDER BY rating DESC
        LIMIT 1
    """)
    best = cursor.fetchone()
    conn.close()
    return best


def get_orders_per_day():
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT created_at::date, COUNT(*) 
        FROM orders 
        GROUP BY created_at::date 
        ORDER BY created_at::date
    """)
    result = cursor.fetchall()
    conn.close()
    return result


def get_top_clients(limit=5):
    conn = connect_to_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT c.name || ' ' || c.surname, COUNT(*) 
        FROM orders o 
        JOIN client c ON o.customer_id = c.id 
        GROUP BY c.id 
        ORDER BY COUNT(*) DESC 
        LIMIT %s
    """, (limit,))
    result = cursor.fetchall()
    conn.close()
    return result