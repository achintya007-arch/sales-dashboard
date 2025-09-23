import pandas as pd
import mysql.connector

def import_csv_to_mysql(csv_file, host, user, password, database):
    df = pd.read_csv(csv_file)

    conn = mysql.connector.connect(
        host=host, port=3306, user=user, password=password,
        database=database, ssl_disabled=False
    )
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales_data (
            order_id INT PRIMARY KEY,
            order_date DATE,
            product_name VARCHAR(255),
            quantity INT,
            price DECIMAL(10,2)
        )
    """)
    cursor.execute("DELETE FROM sales_data")

    insert_sql = """INSERT INTO sales_data 
                    (order_id, order_date, product_name, quantity, price)
                    VALUES (%s, %s, %s, %s, %s)"""
    for _, row in df.iterrows():
        values = (
            int(row['order_id']),
            row['order_date'],
            str(row['product_name']),
            int(row['quantity']),
            float(row['price'])
        )
        cursor.execute(insert_sql, values)

    conn.commit()
    cursor.close()
    conn.close()
    print("✅ Data imported into MySQL successfully!")

def load_data_from_mysql(host, user, password, database):
    conn = mysql.connector.connect(
        host=host, port=3306, user=user, password=password,
        database=database, ssl_disabled=False
    )
    df = pd.read_sql("SELECT * FROM sales_data", conn, parse_dates=["order_date"])
    conn.close()
    return df
