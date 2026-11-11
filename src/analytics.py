
def get_total_revenue(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT SUM(revenue)
        FROM sales
    """)

    total_revenue = cursor.fetchone()[0]

    print("\n--- TOTAL REVENUE ---")
    print("Total Revenue: ₹", total_revenue)



def get_store_revenue(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT store_id, SUM(revenue)
        FROM sales
        GROUP BY store_id
        ORDER BY SUM(revenue) DESC
    """)

    results = cursor.fetchall()

    print("\n--- STORE-WISE REVENUE ---")

    for store in results:
        print(store[0], ":", store[1])


def get_product_revenue(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT product_id, SUM(revenue)
        FROM sales
        GROUP BY product_id
        ORDER BY SUM(revenue) DESC
    """)

    results = cursor.fetchall()

    print("\n--- PRODUCT-WISE REVENUE ---")

    for product in results:
        print(product[0], ":", product[1])


def get_payment_revenue(conn):
    cursor = conn.cursor()

    cursor.execute("""
        SELECT payment_method, SUM(revenue)
        FROM sales
        GROUP BY payment_method
        ORDER BY SUM(revenue) DESC
    """)

    results = cursor.fetchall()

    print("\n--- PAYMENT METHOD-WISE REVENUE ---")

    for payment in results:
        print(payment[0], ":", payment[1])
