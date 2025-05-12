from connection import connect_to_db

# def add_order():
#     try:
#         customer_id = int(input("Enter client ID: "))
#     except ValueError:
#         print("❌ Client ID must be a number.")
#         return

#     order_details = input("Enter order details: ").strip()
#     if not order_details:
#         print("❌ Order details cannot be empty.")
#         return

#     query = "INSERT INTO orders (customer_id, order_details) VALUES (%s, %s);"

#     try:
#         with connect_to_db() as conn:
#             with conn.cursor() as cursor:
#                 cursor.execute(query, (customer_id, order_details))
#             conn.commit()
#         print("✅ Order added successfully.")
#     except Exception as e:
#         print("❌ Error adding order:", e)


def get_orders():
    query = "SELECT * FROM orders"
    try:
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        print("❌ Error fetching orders:", e)
        return []
    
def insert_order(client_id, order_details):
    query = "INSERT INTO orders (customer_id, order_details) VALUES (%s, %s);"
    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, (client_id, order_details))
        conn.commit()


def search_orders(client_id=None, date=None, limit=10, offset=0):
    query = "SELECT * FROM orders WHERE TRUE"
    params = []

    if client_id:
        query += " AND customer_id = %s"
        params.append(client_id)
    if date:
        query += " AND created_at::date = %s"  # assumes created_at exists
        params.append(date)

    query += " ORDER BY id LIMIT %s OFFSET %s"
    params.extend([limit, offset])

    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchall()
        

def count_orders(client_id=None, date=None):
    query = "SELECT COUNT(*) FROM orders WHERE TRUE"
    params = []

    if client_id:
        query += " AND customer_id = %s"
        params.append(client_id)
    if date:
        query += " AND created_at::date = %s"
        params.append(date)

    with connect_to_db() as conn:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            return cursor.fetchone()[0]