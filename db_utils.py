import pandas as pd
import mysql.connector
from mysql.connector import Error

def get_connection(host, user, password, database):
    return mysql.connector.connect(
        host=host,
        port=3306,
        user=user,
        password=password,
        database=database,
        ssl_disabled=False
    )

def import_csv_to_mysql(csv_file, host, user, password, database):
    df = pd.read_csv(csv_file)

    conn = None
    try:
        conn = get_connection(host, user, password, database)
        cursor = conn.cursor()

        # create table if not exists
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS sales_data (
                order_id INT PRIMARY KEY,
                order_date DATE,
                product_name VARCHAR(255),
                quantity INT,
                price DECIMAL(10,2)
            )
        """)
        conn.commit()

        # clear old data
        cursor.execute("DELETE FROM sales_data")
        conn.commit()

        # prepare rows for batch insert
        rows = []
        for _, row in df.iterrows():
            rows.append((
                int(row['order_id']),
                row['order_date'],
                str(row['product_name']),
                int(row['quantity']),
                float(row['price'])
            ))

        insert_sql = """INSERT INTO sales_data 
                        (order_id, order_date, product_name, quantity, price)
                        VALUES (%s, %s, %s, %s, %s)"""
        if rows:
            cursor.executemany(insert_sql, rows)
            conn.commit()

        print("✅ Data imported into MySQL successfully!")
    except Error as e:
        print("MySQL error during import:", e)
        raise
    finally:
        if conn:
            conn.close()

def load_data_from_mysql(host, user, password, database):
    conn = None
    try:
        conn = get_connection(host, user, password, database)
        df = pd.read_sql("SELECT * FROM sales_data", conn, parse_dates=["order_date"]) # type: ignore
        return df
    except Error as e:
        print("MySQL error during load:", e)
        raise
    finally:
        if conn:
            conn.close()
