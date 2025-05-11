from logic.clients import add_client, get_clients
from logic.products import add_product, get_products
from logic.orders import add_order, get_orders

interface = """
1 - Show products
2 - Show clients
3 - Show orders
4 - Add product
5 - Add Client
6 - Add Order
7 - Exit
"""

while True:
    user_input = input(interface)
    if user_input == "1":
        products = get_products()
        for product in products:
            print(product)
    elif user_input == "2":
        clients = get_clients()
        for client in clients:
            print(client)
    elif user_input == "3":
        orders = get_orders()
        for order in orders:
            print(order)
    elif user_input == "4":
        new_products = add_product()
    elif user_input == "5":
        new_client = add_client()
    elif user_input == "6":
        new_order = add_order()
    elif user_input == "7":
        break
