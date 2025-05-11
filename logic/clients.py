from connection import connect_to_db

def add_client():
    first_name = input("Enter client's first name: ").strip()
    last_name = input("Enter client's last name: ").strip()

    if not first_name or not last_name:
        print("❌ First name and last name cannot be empty.")
        return

    query = "INSERT INTO client (name, surname) VALUES (%s, %s);"

    try:
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (first_name, last_name))
            conn.commit()
        print("✅ Client added successfully.")
    except Exception as e:
        print("❌ Error adding client:", e)

def get_clients():
    query = "SELECT * FROM client"
    try:
        with connect_to_db() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
    except Exception as e:
        print("❌ Error fetching clients:", e)
        return []