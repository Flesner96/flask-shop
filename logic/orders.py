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